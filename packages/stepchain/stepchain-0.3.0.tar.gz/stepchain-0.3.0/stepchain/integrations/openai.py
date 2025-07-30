"""Unified LLM client for StepChain.

Provides a consistent interface for OpenAI API interactions.
"""

import logging
from typing import Any, Protocol, runtime_checkable

import openai

from stepchain.config import get_config

logger = logging.getLogger(__name__)


@runtime_checkable
class LLMResponse(Protocol):
    """Protocol for LLM response objects."""
    id: str
    content: str
    tool_calls: list[dict[str, Any]] | None
    usage: dict[str, Any] | None


class UnifiedLLMClient:
    """Unified client for OpenAI Responses API interactions.
    
    Exclusively uses the Responses API with support for tool calls and response chaining.
    """
    
    def __init__(self, api_key: str | None = None):
        """Initialize the LLM client.
        
        Args:
            api_key: Optional API key (defaults to config/env)
        """
        self.config = get_config()
        self.api_key = api_key or self.config.openai_api_key
        self._client: openai.OpenAI | None = None
        self._has_responses_api: bool = False
        
    @property
    def client(self) -> Any:
        """Lazy initialization of OpenAI client."""
        if self._client is None:
            try:
                import openai
            except ImportError:
                raise ImportError(
                    "OpenAI package is required. Install with: pip install openai"
                ) from None
            
            if not self.api_key:
                raise ValueError(
                    "OpenAI API key not found. Set OPENAI_API_KEY environment variable."
                )
            
            self._client = openai.OpenAI(api_key=self.api_key)
            
            # Check if Responses API is available
            self._has_responses_api = hasattr(self._client, 'responses')
            if self._has_responses_api:
                logger.info("OpenAI Responses API detected")
            else:
                logger.error("OpenAI Responses API not detected")
                
        return self._client
    
    def create_completion(
        self,
        prompt: str,
        model: str | None = None,
        tools: list[dict[str, Any]] | None = None,
        previous_response_id: str | None = None,
        tool_outputs: list[dict[str, Any]] | None = None,
        temperature: float = 0.7,
        max_tokens: int | None = None,
        timeout: int | None = None,
    ) -> dict[str, Any]:
        """Create a completion using the appropriate API.
        
        Args:
            prompt: The prompt/input text
            model: Model to use (defaults to config)
            tools: Optional tools/functions
            previous_response_id: ID of previous response (for Responses API)
            tool_outputs: Tool outputs from previous response (required when chaining
                after tool calls)
            temperature: Sampling temperature
            max_tokens: Maximum tokens in response
            timeout: Request timeout in seconds
            
        Returns:
            Standardized response dict with id, content, tool_calls, usage
        """
        # Validate inputs
        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty")
            
        if tools and not isinstance(tools, list):
            raise ValueError("Tools must be a list")
            
        model = model or self.config.openai_model
        timeout = timeout or self.config.openai_timeout
        
        try:
            # Ensure client is initialized (which sets _has_responses_api)
            _ = self.client
            
            # Check if Responses API is available
            if not self._has_responses_api:
                raise ValueError(
                    "Responses API is required for StepChain. "
                    "Please ensure you have the latest OpenAI SDK with Responses API support."
                )
            
            # Use Responses API (with or without previous_response_id)
            result = self._create_response(
                prompt, model, tools, previous_response_id, tool_outputs, timeout
            )
                
            # Final validation
            if not isinstance(result, dict):
                raise ValueError("LLM response must be a dictionary")
                
            if "id" not in result:
                raise ValueError("LLM response missing 'id' field")
                
            if "content" not in result:
                result["content"] = ""
                
            return result
            
        except Exception as e:
            logger.error(f"LLM API call failed: {type(e).__name__}: {str(e)[:200]}")
            # Log full error details for debugging
            if hasattr(e, 'response'):
                logger.error(f"Full error response: {getattr(e.response, 'text', 'No text')}")
            raise
    
    def _create_response(
        self,
        prompt: str,
        model: str,
        tools: list[dict[str, Any]] | None,
        previous_response_id: str | None,
        tool_outputs: list[dict[str, Any]] | None,
        timeout: int,
    ) -> dict[str, Any]:
        """Create completion using Responses API."""
        params = {
            "model": model,
            "input": prompt,
            "store": True,
            "timeout": timeout,
        }
        
        if tools:
            params["tools"] = tools
            
        if previous_response_id:
            params["previous_response_id"] = previous_response_id
            
        if tool_outputs:
            params["tool_outputs"] = tool_outputs
            
        response = self.client.responses.create(**params)
        
        # Validate response object
        if not response:
            raise ValueError("Received null response from OpenAI Responses API")
            
        if not hasattr(response, 'id'):
            raise ValueError("Response missing required 'id' field")
        
        # Log the response structure for debugging
        logger.debug(f"Response object type: {type(response)}")
        logger.debug(f"Response attributes: {dir(response)}")
        
        # Extract content from response - try multiple approaches
        content = ""
        tool_calls = []
        
        # Approach 1: output_text attribute (this is the main text output)
        if hasattr(response, 'output_text') and response.output_text:
            content = response.output_text
            logger.debug(f"Found content in 'output_text' attribute: {len(content)} chars")
        
        # Approach 2: output attribute with structured content
        elif hasattr(response, 'output') and response.output:
            logger.debug(f"Response has 'output' attribute of type: {type(response.output)}")
            
            if isinstance(response.output, list):
                # Handle list of ResponseOutputMessage objects
                for item in response.output:
                    if hasattr(item, 'content') and isinstance(item.content, list):
                        # Extract text from content items
                        for content_item in item.content:
                            if hasattr(content_item, 'text'):
                                content += content_item.text or ""
                    
                    # Extract tool calls if present
                    if hasattr(item, 'tool_calls') and item.tool_calls:
                        tool_calls.extend(item.tool_calls)
        
        
        # Convert content to string if it's not already
        if content and not isinstance(content, str):
            logger.debug(f"Content is {type(content)}, converting to string")
            content = str(content)
        
        # Log extraction results
        content_len = len(content) if isinstance(content, str) else 0
        logger.info(
            f"Extracted from response {response.id}: "
            f"content={content_len} chars, tool_calls={len(tool_calls)}"
        )
        
        # Validate extracted content
        if not content and not tool_calls:
            logger.warning(
                f"Response {response.id} has no content or tool calls - "
                "response may be incomplete"
            )
        
        # Convert tool calls to dict format if needed
        formatted_tool_calls = []
        for tc in tool_calls:
            if isinstance(tc, dict):
                formatted_tool_calls.append(tc)
            elif hasattr(tc, '__dict__'):
                # Convert object to dict
                tc_dict = {
                    "id": getattr(tc, "id", ""),
                    "type": getattr(tc, "type", "function"),
                    "function": {
                        "name": getattr(tc.function, "name", "") if hasattr(tc, "function") else "",
                        "arguments": (
                            getattr(tc.function, "arguments", "{}")
                            if hasattr(tc, "function") else "{}"
                        )
                    }
                }
                formatted_tool_calls.append(tc_dict)
        
        return {
            "id": str(response.id),
            "content": content,
            "tool_calls": formatted_tool_calls if formatted_tool_calls else None,
            "usage": response.usage.model_dump() if hasattr(response, 'usage') else None,
        }


# Global default client
_default_client: UnifiedLLMClient | None = None


def get_default_client() -> UnifiedLLMClient:
    """Get the default LLM client instance."""
    global _default_client
    if _default_client is None:
        _default_client = UnifiedLLMClient()
    return _default_client