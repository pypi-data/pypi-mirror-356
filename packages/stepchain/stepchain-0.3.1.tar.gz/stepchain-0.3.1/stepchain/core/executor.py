"""Executor for running steps with OpenAI Responses API.

This module provides the main execution logic with retry handling.
Supports both OpenAI Responses API and fallback to chat completions.
"""

from contextlib import nullcontext
from datetime import UTC, datetime
from typing import Any

from stepchain.config import get_config
from stepchain.core.models import Plan, Step, StepResult, StepStatus
from stepchain.errors import ExecutionError
from stepchain.function_registry import FunctionRegistry
from stepchain.integrations.openai import UnifiedLLMClient, get_default_client
from stepchain.storage import AbstractStore, JSONLStore
from stepchain.utils.compression import CompressionStrategy, FullHistory
from stepchain.utils.logging import get_logger
from stepchain.utils.retry import classify_error, retry_on_exception
from stepchain.utils.telemetry import Telemetry

logger = get_logger(__name__)


class Executor:
    """Synchronous executor for running plans with OpenAI Responses API.

    Example:
        >>> from unittest.mock import Mock
        >>> client = Mock()
        >>> executor = Executor(client=client)
        >>> plan = Plan(steps=[Step(id="test", prompt="Hello")])
        >>> results = executor.execute_plan(plan, run_id="test_run")
    """

    def __init__(
        self,
        client: UnifiedLLMClient | None = None,
        store: AbstractStore | None = None,
        compression_strategy: CompressionStrategy | None = None,
        telemetry: Telemetry | None = None,
        function_registry: FunctionRegistry | None = None,
    ):
        """Initialize executor.

        Args:
            client: LLM client (defaults to UnifiedLLMClient)
            store: Storage backend (defaults to JSONLStore)
            compression_strategy: History compression (defaults to FullHistory)
            telemetry: Telemetry instance
            function_registry: Registry for custom function execution
        """
        self.config = get_config()
        self.client = client or get_default_client()
        self.store = store or JSONLStore(str(self.config.storage_path))
        self.compression = compression_strategy or FullHistory()
        self.telemetry = (
            telemetry if telemetry is not None
            else (Telemetry() if self.config.enable_telemetry else None)
        )
        self.function_registry = function_registry

    # Removed - now using UnifiedLLMClient

    def execute_plan(
        self,
        plan: Plan,
        run_id: str,
        resume: bool = True,
        tools: list[dict[str, Any]] | None = None,
    ) -> list[StepResult]:
        """Execute a plan, optionally resuming from previous run.

        Args:
            plan: The execution plan
            run_id: Unique identifier for this run
            resume: Whether to resume from previous results
            tools: Optional tools with 'implementation' field for auto-registration

        Returns:
            List of step results
        """
        telemetry_context = (
            self.telemetry.span("execute_plan", {"run_id": run_id, "plan_id": plan.id})
            if self.telemetry else None
        )
        with telemetry_context if telemetry_context else nullcontext():
            plan.validate_dependencies()
            
            # Auto-register functions from tools if provided
            if tools and self.function_registry:
                self.function_registry.register_from_tools(tools)
            
            # Save the plan for future reference
            self.store.save_plan(run_id, plan)
            
            # Get previous results if resuming
            previous_results = self.store.get_results(run_id) if resume else []
            completed_steps = {
                r.step_id for r in previous_results if r.status == StepStatus.COMPLETED
            }
            
            results = []
            for step in plan.steps:
                if step.id in completed_steps:
                    logger.info(f"Skipping completed step: {step.id}")
                    continue
                
                # Check dependencies
                if not all(dep in completed_steps for dep in step.dependencies):
                    logger.warning(f"Skipping {step.id} due to incomplete dependencies")
                    continue
                
                result = self._execute_step(step, run_id, previous_results)
                results.append(result)
                self.store.save_result(run_id, result)
                
                if result.status == StepStatus.COMPLETED:
                    completed_steps.add(step.id)
                    previous_results.append(result)
                else:
                    logger.error(f"Step {step.id} failed, stopping execution")
                    if result.error:
                        raise ExecutionError(step.id, result.error, result.attempt_count)
                    break
            
            return results

    def _execute_step(
        self,
        step: Step,
        run_id: str,
        previous_results: list[StepResult],
    ) -> StepResult:
        """Execute a single step with retries."""
        telemetry_context = (
            self.telemetry.span("execute_step", {"step_id": step.id})
            if self.telemetry else None
        )
        with telemetry_context if telemetry_context else nullcontext():
            result = StepResult(
                step_id=step.id,
                status=StepStatus.RUNNING,
            )
            
            # Get previous response ID from dependencies
            previous_response_id = self._get_previous_response_id(step, previous_results)
            
            @retry_on_exception(max_retries=step.max_retries)
            def run_with_retry() -> dict[str, Any]:
                return self._call_llm(step, previous_results, previous_response_id)
            
            try:
                output = run_with_retry()
                result.status = StepStatus.COMPLETED
                # Ensure output is serializable
                if isinstance(output, dict):
                    result.output = output
                    # Set content from the response
                    result.content = output.get("content", "")
                    # Store tool calls if present
                    if "tool_calls" in output:
                        result.tool_calls = output["tool_calls"]
                        # Execute custom functions if registered
                        if self.function_registry:
                            tool_results = self._execute_tool_calls(output["tool_calls"], step)
                            if tool_results:
                                result.output["tool_results"] = tool_results
                else:
                    # Convert any non-dict response to a dict format
                    result.output = {"content": str(output)}
                    result.content = str(output)
                result.response_id = output.get("response_id") if isinstance(output, dict) else None
                result.previous_response_id = previous_response_id
            except Exception as e:
                error_msg = str(e)[:500]  # Limit error message length
                logger.error(f"Step {step.id} failed after retries: {error_msg}")
                result.status = StepStatus.FAILED
                result.error = error_msg
                result.error_type = classify_error(e)
                result.attempt_count = step.max_retries
            finally:
                result.completed_at = datetime.now(UTC)
                result.calculate_duration()
            
            return result

    def _call_llm(
        self,
        step: Step,
        previous_results: list[StepResult],
        previous_response_id: str | None,
    ) -> dict[str, Any]:
        """Call the LLM with compressed history."""
        # Get formatted input from compression strategy
        input_text = self.compression.compress_to_input(step, previous_results)
        tools = self._format_tools(step.tools)
        
        # Get tool outputs if we're chaining from a previous response
        tool_outputs = None
        if previous_response_id:
            tool_outputs = self._get_tool_outputs_from_previous_step(
                previous_response_id, previous_results
            )
        
        response = self.client.create_completion(
            prompt=input_text,
            tools=tools if tools else None,
            previous_response_id=previous_response_id,
            tool_outputs=tool_outputs,
            timeout=int(step.timeout) if step.timeout else None,
            max_tokens=2000,  # Reasonable default
        )
        
        return response

    def _get_previous_response_id(
        self,
        step: Step,
        previous_results: list[StepResult],
    ) -> str | None:
        """Get the response ID from the last dependency."""
        if not step.dependencies:
            return None
        
        # Find the most recent dependency result
        for dep_id in reversed(step.dependencies):
            for result in reversed(previous_results):
                if result.step_id == dep_id and result.response_id:
                    return result.response_id
        
        return None

    def _get_tool_outputs_from_previous_step(
        self,
        previous_response_id: str | None,
        previous_results: list[StepResult],
    ) -> list[dict[str, Any]] | None:
        """Get tool outputs from the previous step if it had tool calls.
        
        Args:
            previous_response_id: The response ID we're chaining from
            previous_results: All previous step results
            
        Returns:
            List of tool outputs if the previous step had tool calls, None otherwise
        """
        if not previous_response_id:
            return None
        
        # Find the result with this response ID
        for result in reversed(previous_results):
            if result.response_id == previous_response_id:
                if result.tool_calls:
                    # Generate tool outputs for each tool call
                    tool_outputs = []
                    for tool_call in result.tool_calls:
                        # Extract output from the step's output based on tool call
                        tool_id = tool_call.get("id", "")
                        
                        # Try to find corresponding output in the result
                        output_content = ""
                        if result.output:
                            # Check if output has tool-specific results
                            if "tool_results" in result.output:
                                tool_results = result.output["tool_results"]
                                if isinstance(tool_results, dict) and tool_id in tool_results:
                                    output_content = str(tool_results[tool_id])
                                elif isinstance(tool_results, list):
                                    # Find by tool call ID
                                    for tr in tool_results:
                                        if tr.get("tool_call_id") == tool_id:
                                            output_content = tr.get("output", "")
                                            break
                            elif "content" in result.output:
                                # Fallback to general content
                                output_content = result.output["content"]
                        
                        tool_outputs.append({
                            "tool_call_id": tool_id,
                            "output": output_content or "Tool execution completed"
                        })
                    
                    return tool_outputs if tool_outputs else None
                break
        
        return None

    def _format_tools(self, tools: list[str | dict[str, Any]]) -> list[dict[str, Any]] | None:
        """Format tools for the Responses API.
        
        Args:
            tools: List of tool specifications:
                - str: Built-in tool name ("web_search", "code_interpreter", "file_search")
                - dict: MCP server config or custom function definition
                
        Returns:
            Formatted tools list for Responses API or None if no tools
        """
        if not tools:
            return None
            
        formatted = []
        for tool in tools:
            if isinstance(tool, str):
                # Built-in tools
                if tool == "web_search":
                    formatted.append({"type": "web_search"})
                elif tool == "code_interpreter":
                    # Skip code_interpreter - requires container config
                    logger.warning(
                        "code_interpreter requires container configuration, skipping. "
                        "Use dict format with container config instead."
                    )
                elif tool == "file_search":
                    # Skip file_search - requires vector_store_ids
                    logger.warning(
                        "file_search requires vector_store_ids, skipping. "
                        "Use dict format with vector_store_ids instead."
                    )
                else:
                    # Unknown tool - create as function
                    logger.warning(f"Unknown tool '{tool}', creating as function")
                    formatted.append({
                        "type": "function",
                        "name": tool,
                        "description": f"Tool: {tool}",
                        "parameters": {"type": "object", "properties": {}}
                    })
            elif isinstance(tool, dict):
                tool_type = tool.get("type")
                
                if tool_type == "function":
                    # Custom function - flatten if nested
                    if "function" in tool:
                        func = tool["function"]
                        formatted_tool = {
                            "type": "function",
                            "name": func.get("name", "unnamed_function"),
                            "description": func.get("description", ""),
                            "parameters": func.get("parameters", {
                                "type": "object", "properties": {}
                            })
                        }
                        formatted.append(formatted_tool)
                        
                        # Auto-register implementation if provided
                        if "implementation" in tool and self.function_registry:
                            impl = tool["implementation"]
                            name = func.get("name")
                            if name and callable(impl):
                                self.function_registry.register(name, impl)
                    else:
                        # Already flattened
                        formatted.append(tool)
                elif tool_type == "web_search":
                    formatted.append({"type": "web_search"})
                elif tool_type == "code_interpreter":
                    # Pass through with container config
                    if "container" in tool:
                        formatted.append(tool)
                    else:
                        logger.warning("code_interpreter missing container config, skipping")
                elif tool_type == "file_search":
                    # Pass through with vector_store_ids
                    if "vector_store_ids" in tool:
                        formatted.append(tool)
                    else:
                        logger.warning("file_search missing vector_store_ids, skipping")
                elif tool_type == "mcp":
                    # MCP server - keep as-is
                    formatted.append(tool)
                else:
                    # Unknown format - keep as-is
                    logger.warning(f"Unknown tool type: {tool_type}")
                    formatted.append(tool)
            else:
                logger.warning(f"Skipping invalid tool format: {tool}")
                
        return formatted if formatted else None
    
    def _execute_tool_calls(
        self,
        tool_calls: list[dict[str, Any]],
        step: Step,
    ) -> dict[str, Any]:
        """Execute custom function tool calls.
        
        Args:
            tool_calls: List of tool calls from LLM response
            step: The current step (for timeout info)
            
        Returns:
            Dictionary mapping tool_call_id to execution results
        """
        tool_results = {}
        
        for tool_call in tool_calls:
            tool_id = tool_call.get("id", "")
            tool_type = tool_call.get("type")
            
            if tool_type == "function":
                function_name = tool_call.get("function", {}).get("name")
                arguments = tool_call.get("function", {}).get("arguments", {})
                
                if function_name and self.function_registry.get(function_name):
                    try:
                        # Execute the function (registry already has timeout handling)
                        result = self.function_registry.execute(function_name, arguments)
                        tool_results[tool_id] = result
                        logger.info(
                            f"Executed custom function '{function_name}' for tool call {tool_id}"
                        )
                    except Exception as e:
                        # Store error but don't fail the step
                        error_msg = f"Function execution error: {e!s}"
                        tool_results[tool_id] = {"error": error_msg}
                        logger.error(f"Error executing function '{function_name}': {e}")
                else:
                    # No registered function - will use stub output
                    logger.debug(f"No registered function for '{function_name}'")
        
        return tool_results
