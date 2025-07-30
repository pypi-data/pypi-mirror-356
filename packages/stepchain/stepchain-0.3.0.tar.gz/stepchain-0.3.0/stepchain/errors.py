"""Enhanced error classes with helpful messages and troubleshooting hints."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from stepchain.core.models import ErrorType



class StepChainError(Exception):
    """Base exception for StepChain errors."""
    
    def __init__(self, message: str, hint: str | None = None):
        super().__init__(message)
        self.hint = hint
        
    def __str__(self) -> str:
        base = super().__str__()
        if self.hint:
            return f"{base}\nHint: {self.hint}"
        return base


class ConfigurationError(StepChainError):
    """Raised when configuration is invalid or missing."""
    
    def __init__(self, message: str, hint: str | None = None):
        if not hint:
            hint = (
                "Check your environment variables or use setup_stepchain() "
                "for easy configuration"
            )
        super().__init__(message, hint)


class APIKeyError(ConfigurationError):
    """Raised when OpenAI API key is missing or invalid."""
    
    def __init__(self) -> None:
        super().__init__(
            "OpenAI API key not found",
            "Set OPENAI_API_KEY environment variable or use setup_stepchain(api_key='sk-...')"
        )


class DecompositionError(StepChainError):
    """Raised when task decomposition fails."""
    
    def __init__(self, message: str, task: str | None = None):
        hint = "Try simplifying your task description or breaking it into smaller sub-tasks"
        if task and len(task) > 1000:
            hint = "Your task description is very long. Try to be more concise"
        super().__init__(message, hint)


class ExecutionError(StepChainError):
    """Raised when step execution fails."""
    
    def __init__(self, step_id: str, error: str, attempt: int = 1):
        message = f"Step '{step_id}' failed after {attempt} attempt(s): {error}"
        hint = None
        
        if "rate limit" in error.lower():
            hint = (
                "You've hit rate limits. Consider reducing max_concurrent_steps "
                "or upgrading your API tier"
            )
        elif "timeout" in error.lower():
            hint = "Increase timeout in step configuration or simplify the step prompt"
        elif "api key" in error.lower():
            hint = "Check that your API key is valid and has sufficient permissions"
            
        super().__init__(message, hint)


class StorageError(StepChainError):
    """Raised when storage operations fail."""
    
    def __init__(self, message: str, path: str | None = None):
        hint = "Check file permissions and disk space"
        if path:
            hint = f"Ensure you have write permissions for: {path}"
        super().__init__(message, hint)


class ValidationError(StepChainError):
    """Raised when plan or step validation fails."""
    
    def __init__(self, message: str, field: str | None = None):
        hint = "Review the plan structure and ensure all required fields are present"
        if field:
            hint = f"Check the '{field}' field in your plan or step configuration"
        super().__init__(message, hint)


class StepExecutionError(ExecutionError):
    """Specific error for step execution failures."""
    
    def __init__(self, step_id: str, message: str, error_type: ErrorType | None = None):
        super().__init__(step_id, message)
        self.error_type = error_type
        
        
def get_error_type(error_msg: str) -> ErrorType:
    """Classify error message into error type."""
    from stepchain.core.models import ErrorType
    
    error_lower = error_msg.lower()
    
    if "rate limit" in error_lower:
        return ErrorType.RATE_LIMIT
    elif any(term in error_lower for term in ["network", "connection", "timeout"]):
        return ErrorType.NETWORK
    elif any(term in error_lower for term in [
        "500", "502", "503", "server error", "internal server"
    ]):
        return ErrorType.SERVER_ERROR
    elif any(term in error_lower for term in ["tool", "function"]):
        return ErrorType.TOOL_ERROR
    else:
        return ErrorType.OTHER