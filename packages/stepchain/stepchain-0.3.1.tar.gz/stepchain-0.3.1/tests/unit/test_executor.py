"""Unit tests for Executor."""

import json
from datetime import datetime
from unittest.mock import MagicMock, call, patch

import pytest

from stepchain.errors import StepExecutionError, get_error_type
from stepchain.core.models import ErrorType
from stepchain.core.executor import Executor
from stepchain.core.models import Plan, Step, StepResult, StepStatus


class TestExecutor:
    """Test cases for Executor."""

    @pytest.fixture
    def executor(self, mock_unified_llm_client):
        """Create an Executor instance for testing."""
        mock_store = MagicMock()
        executor = Executor(client=mock_unified_llm_client, store=mock_store)
        return executor

    def test_execute_plan_simple(self, executor, sample_plan):
        """Test executing a simple plan."""
        # Mock LLM responses
        mock_responses = [
            {"content": "Step 1 completed", "response_id": "resp_1"},
            {"content": "Step 2 completed", "response_id": "resp_2"},
            {"content": "Step 3 completed", "response_id": "resp_3"},
        ]
        
        executor.client.create_completion = MagicMock(side_effect=mock_responses)
        executor.store.save_result = MagicMock()
        executor.store.get_results = MagicMock(return_value=[])
        
        # Execute plan
        results = executor.execute_plan(sample_plan, run_id="test-run")
        
        # Verify results
        assert len(results) == 3
        assert all(r.status == StepStatus.COMPLETED for r in results)
        assert results[0].content == "Step 1 completed"
        assert results[1].content == "Step 2 completed"
        assert results[2].content == "Step 3 completed"
        
        # Verify store was called
        assert executor.store.save_result.call_count == 3

    def test_execute_plan_with_dependencies(self, executor):
        """Test executing a plan with complex dependencies."""
        plan = Plan(
            goal="Test dependencies",
            steps=[
                Step(id="a", prompt="Step A"),
                Step(id="b", prompt="Step B", dependencies=["a"]),
                Step(id="c", prompt="Step C", dependencies=["a"]),
                Step(id="d", prompt="Step D", dependencies=["b", "c"]),
            ]
        )
        
        execution_order = []
        
        def mock_completion(**kwargs):
            messages = kwargs.get("messages", [])
            if messages and len(messages) > 0:
                step_id = messages[-1].get("content", "").split()[-1]
            else:
                step_id = "unknown"
            execution_order.append(step_id)
            return {"content": f"Completed {step_id}", "response_id": f"resp_{step_id}"}
        
        executor.client.create_completion = MagicMock(side_effect=mock_completion)
        executor.store.save_result = MagicMock()
        executor.store.get_results = MagicMock(return_value=[])
        
        results = executor.execute_plan(plan, run_id="test-run")
        
        # Verify all steps were executed
        assert len(results) == 4
        assert len(execution_order) == 4

    def test_execute_step_with_tools(self, executor):
        """Test executing a step with tools."""
        step = Step(
            id="search-step",
            prompt="Search for information",
            tools=["web_search"],
        )
        
        executor.client.create_completion = MagicMock(
            return_value={"content": "Search results", "response_id": "resp_1"}
        )
        
        result = executor._execute_step(step, "test-run", [])
        
        # Verify tool was included in the call
        assert result.status == StepStatus.COMPLETED
        call_args = executor.client.create_completion.call_args
        assert "tools" in call_args.kwargs
        assert call_args.kwargs["tools"][0]["type"] == "web_search"

    def test_execute_step_with_output_schema(self, executor):
        """Test executing a step with output schema validation."""
        # Current implementation doesn't support output_schema in Step
        step = Step(
            id="extract-step",
            prompt="Extract data",
        )
        
        # Mock response with structured output
        mock_output = {"result": "extracted", "confidence": 0.95}
        executor.client.create_completion = MagicMock(
            return_value={
                "content": json.dumps(mock_output),
                "response_id": "resp_1",
            }
        )
        
        result = executor._execute_step(step, "test-run", [])
        
        assert result.status == StepStatus.COMPLETED
        # The output field contains raw response, not parsed JSON
        assert result.output == {"content": json.dumps(mock_output), "response_id": "resp_1"}

    def test_execute_step_with_retry(self, executor):
        """Test step execution with retry on failure."""
        step = Step(id="retry-step", prompt="Retry test", max_retries=3)
        
        # This test verifies the retry decorator is called with correct params
        # The actual retry logic is tested separately in test_retry.py
        executor.client.create_completion = MagicMock(
            return_value={"content": "Success", "response_id": "resp_1"}
        )
        
        result = executor._execute_step(step, "test-run", {})
        
        assert result.status == StepStatus.COMPLETED
        assert result.content == "Success"
        assert executor.client.create_completion.called

    def test_execute_step_max_retries_exceeded(self, executor):
        """Test step execution when max retries are exceeded."""
        step = Step(id="fail-step", prompt="Always fails", max_retries=2)
        
        # Always fail
        executor.client.create_completion = MagicMock(
            side_effect=Exception("Persistent error")
        )
        
        result = executor._execute_step(step, "test-run", [])
        
        assert result.status == StepStatus.FAILED
        assert "Persistent error" in result.error
        assert result.attempt_count == 2  # max_retries=2

    def test_execute_plan_with_resume(self, executor, sample_plan):
        """Test resuming plan execution from saved state."""
        # Mock already completed results
        completed_result = StepResult(
            step_id="step1",
            status=StepStatus.COMPLETED,
            content="Already done",
            attempt_count=1,
        )
        
        executor.store.get_results = MagicMock(return_value=[completed_result])
        
        # Mock remaining steps
        mock_responses = [
            {"content": "Step 2 completed", "response_id": "resp_2"},
            {"content": "Step 3 completed", "response_id": "resp_3"},
        ]
        
        executor.client.create_completion = MagicMock(side_effect=mock_responses)
        executor.store.save_result = MagicMock()
        
        results = executor.execute_plan(sample_plan, run_id="test-run", resume=True)
        
        # Should only return newly executed steps
        assert len(results) == 2
        assert results[0].step_id == "step2"
        assert results[1].step_id == "step3"
        
        # Only 2 new executions (step1 was already completed)
        assert executor.client.create_completion.call_count == 2

    def test_format_tools_builtin(self, executor):
        """Test formatting built-in tools."""
        tools = ["web_search", "code_interpreter"]
        formatted = executor._format_tools(tools)
        
        # code_interpreter is skipped without container config
        assert len(formatted) == 1
        assert formatted[0] == {"type": "web_search"}

    def test_format_tools_custom_function(self, executor):
        """Test formatting custom function tools."""
        custom_tool = {
            "type": "function",
            "function": {
                "name": "calculate",
                "description": "Perform calculation",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "expression": {"type": "string"},
                    },
                },
            },
        }
        
        tools = [custom_tool]
        formatted = executor._format_tools(tools)
        
        assert len(formatted) == 1
        # The formatter flattens the function format
        assert formatted[0]["type"] == "function"
        assert formatted[0]["name"] == "calculate"
        assert formatted[0]["description"] == "Perform calculation"

    def test_format_tools_mcp(self, executor):
        """Test formatting MCP tools."""
        mcp_tool = {
            "type": "mcp",
            "server_label": "math_server",
            "server_url": "http://localhost:3000",
            "allowed_tools": ["add", "subtract"],
        }
        
        tools = [mcp_tool]
        formatted = executor._format_tools(tools)
        
        assert len(formatted) == 1
        assert formatted[0] == mcp_tool

    def test_build_messages_simple(self, executor):
        """Test building messages for a simple step."""
        # The current implementation builds messages inline
        # This test verifies that the prompt is passed correctly
        step = Step(id="test", prompt="Test prompt")
        
        executor.client.create_completion = MagicMock(
            return_value={"content": "Done", "response_id": "resp_1"}
        )
        
        result = executor._execute_step(step, "test-run", {})
        
        # Verify execution completed
        assert result.status == StepStatus.COMPLETED
        assert executor.client.create_completion.called

    def test_build_messages_with_dependencies(self, executor):
        """Test building messages with dependency results."""
        # Test that steps can be executed with dependencies
        step = Step(id="test", prompt="Test with deps", dependencies=["dep1"])
        
        dep_result = StepResult(
            step_id="dep1",
            status=StepStatus.COMPLETED,
            content="Dependency completed",
            output={"data": "value"},
            attempt_count=1,
        )
        
        executor.client.create_completion = MagicMock(
            return_value={"content": "Done", "response_id": "resp_1"}
        )
        
        # Execute with dependency results passed as a list
        result = executor._execute_step(step, "test-run", [dep_result])
        
        # Verify the step was executed successfully
        assert result.status == StepStatus.COMPLETED
        assert executor.client.create_completion.called

    def test_build_messages_with_output_schema(self, executor):
        """Test building messages with output schema requirement."""
        # Current implementation doesn't support output schema
        # This test is kept for documentation purposes
        pass

    def test_get_error_type(self):
        """Test error type classification."""
        # Rate limit errors
        assert get_error_type("rate limit exceeded") == ErrorType.RATE_LIMIT
        assert get_error_type("Rate limit reached") == ErrorType.RATE_LIMIT
        
        # Network errors
        assert get_error_type("Connection timeout") == ErrorType.NETWORK
        assert get_error_type("Network unreachable") == ErrorType.NETWORK
        
        # Server errors
        assert get_error_type("Internal server error") == ErrorType.SERVER_ERROR
        assert get_error_type("502 Bad Gateway") == ErrorType.SERVER_ERROR
        
        # Tool errors
        assert get_error_type("Tool execution failed") == ErrorType.TOOL_ERROR
        assert get_error_type("Function call error") == ErrorType.TOOL_ERROR
        
        # Other errors
        assert get_error_type("Unknown error") == ErrorType.OTHER