"""Function registry for executing custom tool functions."""

import json
import logging
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from typing import Any, Protocol

logger = logging.getLogger(__name__)


class ToolFunction(Protocol):
    """Protocol for tool functions."""
    
    def __call__(self, **kwargs: Any) -> Any:
        """Execute the function with keyword arguments."""
        ...


class FunctionRegistry:
    """Registry for custom tool functions that can be executed by the SDK."""
    
    def __init__(self, timeout: float = 30.0):
        """Initialize the function registry.
        
        Args:
            timeout: Maximum execution time for functions in seconds
        """
        self._functions: dict[str, ToolFunction] = {}
        self._timeout = timeout
        self._executor = ThreadPoolExecutor(max_workers=1)
    
    def register(self, name: str, func: ToolFunction) -> None:
        """Register a function for execution.
        
        Args:
            name: Function name (must match tool name)
            func: Callable to execute
        """
        if not callable(func):
            raise ValueError(f"Function {name} must be callable")
        
        self._functions[name] = func
        logger.info(f"Registered function: {name}")
    
    def get(self, name: str) -> ToolFunction | None:
        """Get a registered function by name.
        
        Args:
            name: Function name
            
        Returns:
            The function if registered, None otherwise
        """
        return self._functions.get(name)
    
    def execute(self, name: str, arguments: dict[str, Any]) -> Any:
        """Execute a registered function with arguments.
        
        Args:
            name: Function name
            arguments: Arguments to pass to the function
            
        Returns:
            Function result (must be JSON serializable)
            
        Raises:
            ValueError: If function not found or execution fails
            TimeoutError: If function execution exceeds timeout
        """
        func = self.get(name)
        if not func:
            raise ValueError(f"Function '{name}' not registered")
        
        try:
            # Execute with timeout
            future = self._executor.submit(func, **arguments)
            result = future.result(timeout=self._timeout)
            
            # Ensure result is JSON serializable
            json.dumps(result)
            
            return result
            
        except TimeoutError:
            future.cancel()
            raise TimeoutError(
                f"Function '{name}' execution exceeded {self._timeout}s timeout"
            ) from None
        except Exception as e:
            logger.error(f"Error executing function '{name}': {e}")
            raise ValueError(f"Function execution failed: {e!s}") from e
    
    def register_from_tools(self, tools: list[dict[str, Any]]) -> None:
        """Register functions from tool definitions.
        
        Looks for 'implementation' key in tool definitions.
        
        Args:
            tools: List of tool definitions
        """
        for tool in tools:
            if tool.get("type") == "function" and "implementation" in tool:
                func_def = tool.get("function", {})
                name = func_def.get("name")
                impl = tool["implementation"]
                
                if name and callable(impl):
                    self.register(name, impl)
    
    def __del__(self) -> None:
        """Cleanup executor on deletion."""
        if hasattr(self, '_executor'):
            self._executor.shutdown(wait=False)