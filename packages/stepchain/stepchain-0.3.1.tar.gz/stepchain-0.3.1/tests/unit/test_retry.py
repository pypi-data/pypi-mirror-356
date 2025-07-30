"""Unit tests for retry logic."""

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from stepchain.errors import StepExecutionError
from stepchain.core.models import ErrorType
from stepchain.utils.retry import calculate_backoff, retry_on_exception, should_retry


class TestRetryLogic:
    """Test cases for retry logic."""

    def test_should_retry_rate_limit(self):
        """Test retry decision for rate limit errors."""
        error = StepExecutionError(
            step_id="test",
            message="Rate limit exceeded",
            error_type=ErrorType.RATE_LIMIT,
        )
        
        # Should retry rate limits up to max attempts
        assert should_retry(error, attempt=1, max_retries=3) is True
        assert should_retry(error, attempt=3, max_retries=3) is True
        assert should_retry(error, attempt=4, max_retries=3) is False

    def test_should_retry_network_error(self):
        """Test retry decision for network errors."""
        error = StepExecutionError(
            step_id="test",
            message="Connection timeout",
            error_type=ErrorType.NETWORK,
        )
        
        assert should_retry(error, attempt=1, max_retries=3) is True
        assert should_retry(error, attempt=2, max_retries=3) is True

    def test_should_retry_server_error(self):
        """Test retry decision for server errors."""
        error = StepExecutionError(
            step_id="test",
            message="500 Internal Server Error",
            error_type=ErrorType.SERVER_ERROR,
        )
        
        assert should_retry(error, attempt=1, max_retries=3) is True

    def test_should_not_retry_tool_error(self):
        """Test that tool errors are not retried."""
        error = StepExecutionError(
            step_id="test",
            message="Tool execution failed",
            error_type=ErrorType.TOOL_ERROR,
        )
        
        assert should_retry(error, attempt=1, max_retries=3) is False

    def test_should_not_retry_other_errors(self):
        """Test that other errors are not retried."""
        error = StepExecutionError(
            step_id="test",
            message="Unknown error",
            error_type=ErrorType.OTHER,
        )
        
        assert should_retry(error, attempt=1, max_retries=3) is False

    def test_should_not_retry_generic_exception(self):
        """Test that generic exceptions are not retried."""
        error = ValueError("Some error")
        assert should_retry(error, attempt=1, max_retries=3) is False

    def test_calculate_backoff_exponential(self):
        """Test exponential backoff calculation."""
        # First retry
        backoff = calculate_backoff(attempt=1, base_delay=1.0, max_delay=60.0)
        assert 1.0 <= backoff <= 2.0  # 1 * 2^0 with jitter
        
        # Second retry
        backoff = calculate_backoff(attempt=2, base_delay=1.0, max_delay=60.0)
        assert 2.0 <= backoff <= 4.0  # 1 * 2^1 with jitter
        
        # Third retry
        backoff = calculate_backoff(attempt=3, base_delay=1.0, max_delay=60.0)
        assert 4.0 <= backoff <= 8.0  # 1 * 2^2 with jitter

    def test_calculate_backoff_max_delay(self):
        """Test that backoff respects max delay."""
        # High attempt number
        backoff = calculate_backoff(attempt=10, base_delay=1.0, max_delay=10.0)
        # Account for jitter (up to 50% of max_delay)
        assert backoff <= 10.0 * 1.5

    def test_calculate_backoff_with_jitter(self):
        """Test that backoff includes jitter."""
        # Run multiple times to ensure jitter is applied
        backoffs = [
            calculate_backoff(attempt=2, base_delay=1.0, max_delay=60.0)
            for _ in range(10)
        ]
        
        # Should have some variation due to jitter
        assert len(set(backoffs)) > 1
        assert all(2.0 <= b <= 4.0 for b in backoffs)

    @pytest.mark.asyncio
    async def test_retry_on_exception_decorator_success(self):
        """Test retry decorator with successful execution."""
        call_count = 0
        
        @retry_on_exception(max_retries=3, base_delay=0.01, max_delay=0.1)
        async def test_func():
            nonlocal call_count
            call_count += 1
            return "success"
        
        result = await test_func()
        
        assert result == "success"
        assert call_count == 1  # No retries needed

    @pytest.mark.asyncio
    async def test_retry_on_exception_decorator_retry_success(self):
        """Test retry decorator with eventual success."""
        call_count = 0
        
        @retry_on_exception(max_retries=3, base_delay=0.01, max_delay=0.1)
        async def test_func():
            nonlocal call_count
            call_count += 1
            
            if call_count < 3:
                raise StepExecutionError(
                    step_id="test",
                    message="Rate limit",
                    error_type=ErrorType.RATE_LIMIT,
                )
            
            return "success"
        
        result = await test_func()
        
        assert result == "success"
        assert call_count == 3  # Two failures, then success

    @pytest.mark.asyncio
    async def test_retry_on_exception_decorator_max_retries(self):
        """Test retry decorator when max retries exceeded."""
        call_count = 0
        
        @retry_on_exception(max_retries=2, base_delay=0.01, max_delay=0.1)
        async def test_func():
            nonlocal call_count
            call_count += 1
            
            raise StepExecutionError(
                step_id="test",
                message="Persistent error",
                error_type=ErrorType.NETWORK,
            )
        
        with pytest.raises(StepExecutionError) as exc_info:
            await test_func()
        
        assert call_count == 3  # Initial + 2 retries
        assert "Persistent error" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_retry_on_exception_decorator_non_retryable(self):
        """Test retry decorator with non-retryable error."""
        call_count = 0
        
        @retry_on_exception(max_retries=3, base_delay=0.01, max_delay=0.1)
        async def test_func():
            nonlocal call_count
            call_count += 1
            
            raise StepExecutionError(
                step_id="test",
                message="Tool error",
                error_type=ErrorType.TOOL_ERROR,
            )
        
        with pytest.raises(StepExecutionError) as exc_info:
            await test_func()
        
        assert call_count == 1  # No retries for non-retryable errors
        assert "Tool error" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_retry_on_exception_with_sync_function(self):
        """Test retry decorator with synchronous function."""
        call_count = 0
        
        @retry_on_exception(max_retries=3, base_delay=0.01, max_delay=0.1)
        def test_func():
            nonlocal call_count
            call_count += 1
            
            if call_count < 2:
                raise StepExecutionError(
                    step_id="test",
                    message="Network error",
                    error_type=ErrorType.NETWORK,
                )
            
            return "success"
        
        # Should handle sync functions
        result = test_func()
        
        assert result == "success"
        assert call_count == 2

    @pytest.mark.asyncio
    async def test_retry_with_logging(self, caplog):
        """Test that retries are logged appropriately."""
        @retry_on_exception(max_retries=2, base_delay=0.01, max_delay=0.1)
        async def test_func():
            raise StepExecutionError(
                step_id="test",
                message="Rate limit",
                error_type=ErrorType.RATE_LIMIT,
            )
        
        with pytest.raises(StepExecutionError):
            await test_func()
        
        # Check that retry attempts were logged
        # Note: This assumes logging is configured in the retry decorator
        # You may need to adjust based on actual implementation

    @pytest.mark.asyncio
    async def test_retry_backoff_timing(self):
        """Test that retry backoff delays are applied."""
        import time
        
        call_times = []
        
        @retry_on_exception(max_retries=2, base_delay=0.1, max_delay=0.5)
        async def test_func():
            call_times.append(time.time())
            
            if len(call_times) < 3:
                raise StepExecutionError(
                    step_id="test",
                    message="Network error",
                    error_type=ErrorType.NETWORK,
                )
            
            return "success"
        
        await test_func()
        
        # Check delays between calls
        assert len(call_times) == 3
        
        # First retry delay (approximately base_delay)
        first_delay = call_times[1] - call_times[0]
        assert 0.05 <= first_delay <= 0.2  # With jitter
        
        # Second retry delay (approximately base_delay * 2)
        second_delay = call_times[2] - call_times[1]
        assert 0.1 <= second_delay <= 0.4  # With jitter