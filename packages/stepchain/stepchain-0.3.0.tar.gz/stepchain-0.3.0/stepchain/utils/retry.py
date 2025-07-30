"""Retry strategies and error classification.

This module provides intelligent retry logic based on error types.
"""

import logging
import re
import time
from collections.abc import Callable
from typing import Any, TypeVar

from stepchain.core.models import ErrorType

logger = logging.getLogger(__name__)

T = TypeVar("T")


def classify_error(exception: Exception) -> ErrorType:
    """Classify an exception into an error type for retry strategies.

    Example:
        >>> from openai import RateLimitError
        >>> classify_error(RateLimitError("Too many requests"))
        <ErrorType.RATE_LIMIT: 'rate_limit'>
    """
    error_msg = str(exception).lower()
    
    # Check for OpenAI-specific errors
    if hasattr(exception, '__class__'):
        class_name = exception.__class__.__name__
        if 'RateLimitError' in class_name:
            return ErrorType.RATE_LIMIT
        if 'APIError' in class_name and hasattr(exception, 'status_code'):
            if exception.status_code == 429:
                return ErrorType.RATE_LIMIT
            elif exception.status_code >= 500:
                return ErrorType.SERVER_ERROR

    # Rate limit errors
    if "rate" in error_msg and "limit" in error_msg:
        return ErrorType.RATE_LIMIT
    if "429" in error_msg or "too many requests" in error_msg:
        return ErrorType.RATE_LIMIT
    if "quota" in error_msg and "exceeded" in error_msg:
        return ErrorType.RATE_LIMIT

    # Server errors
    if any(code in error_msg for code in ["500", "502", "503", "504"]):
        return ErrorType.SERVER_ERROR
    if "server" in error_msg and "error" in error_msg:
        return ErrorType.SERVER_ERROR
    if "service" in error_msg and "unavailable" in error_msg:
        return ErrorType.SERVER_ERROR

    # Tool errors
    if "tool" in error_msg and ("failed" in error_msg or "error" in error_msg):
        return ErrorType.TOOL_ERROR
    if "function_call" in error_msg and "failed" in error_msg:
        return ErrorType.TOOL_ERROR

    # User errors (likely won't retry)
    if any(term in error_msg for term in
           ["invalid", "unauthorized", "forbidden", "400", "401", "403"]):
        return ErrorType.USER_ERROR
    if "authentication" in error_msg or "api key" in error_msg:
        return ErrorType.USER_ERROR

    return ErrorType.UNKNOWN


def calculate_backoff(attempt: int, base_delay: float = 1.0, max_delay: float = 60.0) -> float:
    """Calculate exponential backoff with jitter.
    
    Args:
        attempt: Attempt number (1-based)
        base_delay: Base delay in seconds
        max_delay: Maximum delay in seconds
        
    Returns:
        Backoff time in seconds with jitter
    """
    import random
    
    # Exponential backoff: base_delay * 2^(attempt-1)
    delay = base_delay * (2 ** (attempt - 1))
    
    # Cap at max_delay
    delay = min(delay, max_delay)
    
    # Add jitter (0-50% of delay)
    jitter = delay * random.random() * 0.5
    
    return delay + jitter


def should_retry(error: Exception | ErrorType, attempt: int, max_retries: int) -> bool:
    """Determine if an error should be retried.

    Args:
        error: Exception or ErrorType
        attempt: Current attempt number (1-based)
        max_retries: Maximum number of retries allowed
        
    Returns:
        True if should retry, False otherwise
    """
    from stepchain.errors import StepExecutionError
    
    if attempt > max_retries:
        return False
        
    # Get error type
    if isinstance(error, ErrorType):
        error_type = error
    elif isinstance(error, StepExecutionError) and error.error_type:
        error_type = error.error_type
    elif isinstance(error, Exception):
        error_type = classify_error(error)
    else:
        return False
        
    # Only retry certain error types
    return error_type in {ErrorType.RATE_LIMIT, ErrorType.SERVER_ERROR, ErrorType.NETWORK}


def get_retry_wait_time(
    error_type: ErrorType, attempt: int, retry_after: int | None = None
) -> float:
    """Calculate wait time for retry based on error type and attempt number.
    
    Args:
        error_type: The type of error
        attempt: Current attempt number (0-based)
        retry_after: Optional retry-after header value in seconds
        
    Returns:
        Wait time in seconds
    """
    if retry_after is not None and retry_after > 0:
        # Respect retry-after header with a small buffer
        return retry_after + 0.5
    
    if error_type == ErrorType.RATE_LIMIT:
        # Exponential backoff for rate limits: 4, 8, 16, 32, 60
        return float(min(4 * (2 ** attempt), 60))
    elif error_type == ErrorType.SERVER_ERROR:
        # Exponential backoff for server errors: 2, 4, 8, 16, 30  
        return float(min(2 * (2 ** attempt), 30))
    elif error_type == ErrorType.TOOL_ERROR:
        # Fixed 2 second wait for tool errors
        return 2.0
    else:
        # Default exponential backoff: 1, 2, 4, 8, 10
        return float(min(2 ** attempt, 10))


def extract_retry_after(exception: Exception) -> int | None:
    """Extract retry-after value from exception headers if available.
    
    Args:
        exception: The exception to check
        
    Returns:
        Retry-after value in seconds, or None if not found
    """
    # Check for OpenAI API exceptions with headers
    if hasattr(exception, 'response') and hasattr(exception.response, 'headers'):
        retry_after = exception.response.headers.get('retry-after')
        if retry_after:
            try:
                return int(retry_after)
            except ValueError:
                logger.warning(f"Invalid retry-after header value: {retry_after}")
    
    # Check for retry-after in error message
    error_msg = str(exception)
    match = re.search(r'retry[_-]?after["\s:]+([0-9]+)', error_msg, re.IGNORECASE)
    if match:
        try:
            return int(match.group(1))
        except ValueError:
            pass
    
    return None


def retry_on_exception(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    classify_func: Callable[[Exception], ErrorType] | None = None,
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Decorator for retrying functions with smart error classification.

    Example:
        >>> @retry_on_exception(max_attempts=5)
        ... def call_api():
        ...     # Make API call
        ...     pass
    """
    import asyncio
    import inspect
    
    if classify_func is None:
        classify_func = classify_error
    
    if max_retries < 0:
        raise ValueError("max_retries must be at least 0")

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        async def async_wrapper(*args: Any, **kwargs: Any) -> T:
            last_exception = None
            
            for attempt in range(1, max_retries + 2):  # 1-based attempts
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    
                    if not should_retry(e, attempt, max_retries):
                        raise
                    
                    # Calculate backoff
                    wait_time = calculate_backoff(attempt, base_delay, max_delay)
                    logger.info(
                        f"Retrying after {wait_time:.2f}s "
                        f"(attempt {attempt}/{max_retries + 1})"
                    )
                    await asyncio.sleep(wait_time)
            
            if last_exception:
                raise last_exception
            raise RuntimeError("Unexpected retry loop termination")
        
        def sync_wrapper(*args: Any, **kwargs: Any) -> T:
            last_exception = None
            
            for attempt in range(1, max_retries + 2):  # 1-based attempts  
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    
                    if not should_retry(e, attempt, max_retries):
                        raise
                    
                    # Calculate backoff
                    wait_time = calculate_backoff(attempt, base_delay, max_delay)
                    logger.info(
                        f"Retrying after {wait_time:.2f}s "
                        f"(attempt {attempt}/{max_retries + 1})"
                    )
                    time.sleep(wait_time)
            
            if last_exception:
                raise last_exception
            raise RuntimeError("Unexpected retry loop termination")
        
        # Return appropriate wrapper based on function type
        if inspect.iscoroutinefunction(func):
            return async_wrapper  # type: ignore
        else:
            return sync_wrapper  # type: ignore

    return decorator
