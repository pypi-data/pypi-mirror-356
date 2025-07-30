"""Unit tests for Executor."""

import json
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, call, patch

import pytest

from stepchain.errors import StepExecutionError, get_error_type
from stepchain.core.models import ErrorType
from stepchain.core.executor import Executor
from stepchain.core.models import Plan, Step, StepResult, StepStatus


class TestExecutor:
    """Test cases for Executor."""

    @pytest.fixture
    async def executor(self, mock_config, mock_unified_llm_client):
        """Create an Executor instance for testing."""
        with patch("stepchain.core.executor.JSONLStore") as mock_store:
            executor = Executor(config=mock_config)
            executor.store = mock_store
            yield executor

    @pytest.mark.asyncio
    async def test_execute_plan_simple(self, executor, sample_plan):
        """Test executing a simple plan."""
        # Mock LLM responses
        mock_responses = [
            {"content": "Step 1 completed", "response_id": "resp_1"},
            {"content": "Step 2 completed", "response_id": "resp_2"},
            {"content": "Step 3 completed", "response_id": "resp_3"},
        ]
        
        executor.llm_client.create_completion = AsyncMock(side_effect=mock_responses)
        executor.store.save_result = MagicMock()
        executor.store.get_results = MagicMock(return_value=[])
        
        # Execute plan
        results = await executor.execute_plan(sample_plan, run_id="test-run")
        
        # Verify results
        assert len(results) == 3
        assert all(r.status == StepStatus.COMPLETED for r in results)
        assert results[0].content == "Step 1 completed"
        assert results[1].content == "Step 2 completed"
        assert results[2].content == "Step 3 completed"
        
        # Verify store was called
        assert executor.store.save_result.call_count == 3

    @pytest.mark.asyncio
    async def test_execute_plan_with_dependencies(self, executor):
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
        
        async def mock_completion(**kwargs):
            step_id = kwargs.get("messages", [{}])[0].get("content", "").split()[-1]
            execution_order.append(step_id)
            return {"content": f"Completed {step_id}", "response_id": f"resp_{step_id}"}
        
        executor.llm_client.create_completion = AsyncMock(side_effect=mock_completion)
        executor.store.save_result = MagicMock()
        executor.store.get_results = MagicMock(return_value=[])
        
        results = await executor.execute_plan(plan, run_id="test-run")
        
        # Verify execution order respects dependencies
        assert execution_order.index("A") < execution_order.index("B")
        assert execution_order.index("A") < execution_order.index("C")
        assert execution_order.index("B") < execution_order.index("D")
        assert execution_order.index("C") < execution_order.index("D")

    @pytest.mark.asyncio
    async def test_execute_step_with_tools(self, executor, mock_config):
        """Test executing a step with tools."""
        step = Step(
            id="search-step",
            prompt="Search for information",
            tools=["web_search"],
        )
        
        executor.llm_client.create_completion = AsyncMock(
            return_value={"content": "Search results", "response_id": "resp_1"}
        )
        
        result = await executor._execute_step(step, {}, "test-run", mock_config)
        
        # Verify tool was included in the call
        call_args = executor.llm_client.create_completion.call_args
        assert "tools" in call_args.kwargs
        assert call_args.kwargs["tools"][0]["type"] == "web_search"

    @pytest.mark.asyncio
    async def test_execute_step_with_output_schema(self, executor, mock_config):
        """Test executing a step with output schema validation."""
        output_schema = {
            "type": "object",
            "properties": {
                "result": {"type": "string"},
                "confidence": {"type": "number"},
            },
        }
        
        step = Step(
            id="extract-step",
            prompt="Extract data",
            output_schema=output_schema,
        )
        
        # Mock response with structured output
        mock_output = {"result": "extracted", "confidence": 0.95}
        executor.llm_client.create_completion = AsyncMock(
            return_value={
                "content": json.dumps(mock_output),
                "response_id": "resp_1",
            }
        )
        
        result = await executor._execute_step(step, {}, "test-run", mock_config)
        
        assert result.status == StepStatus.COMPLETED
        assert result.output == mock_output

    @pytest.mark.asyncio
    async def test_execute_step_with_retry(self, executor, mock_config):
        """Test step execution with retry on failure."""
        step = Step(id="retry-step", prompt="Retry test")
        
        # First two calls fail, third succeeds
        executor.llm_client.create_completion = AsyncMock(
            side_effect=[
                Exception("Network error"),
                Exception("Rate limit"),
                {"content": "Success", "response_id": "resp_1"},
            ]
        )
        
        with patch("stepchain.core.executor.retry_on_exception") as mock_retry:
            # Make retry_on_exception pass through the function
            mock_retry.side_effect = lambda f: f
            
            result = await executor._execute_step(step, {}, "test-run", mock_config)
            
            assert result.status == StepStatus.COMPLETED
            assert result.content == "Success"
            assert executor.llm_client.create_completion.call_count == 3

    @pytest.mark.asyncio
    async def test_execute_step_max_retries_exceeded(self, executor, mock_config):
        """Test step execution when max retries are exceeded."""
        step = Step(id="fail-step", prompt="Always fails")
        
        # Always fail
        executor.llm_client.create_completion = AsyncMock(
            side_effect=Exception("Persistent error")
        )
        
        # Mock config with low retry count
        mock_config.max_retries = 2
        
        result = await executor._execute_step(step, {}, "test-run", mock_config)
        
        assert result.status == StepStatus.FAILED
        assert "Persistent error" in result.error
        assert result.attempt_count == 3  # Initial + 2 retries

    @pytest.mark.asyncio
    async def test_execute_plan_with_resume(self, executor, sample_plan):
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
        
        executor.llm_client.create_completion = AsyncMock(side_effect=mock_responses)
        executor.store.save_result = MagicMock()
        
        results = await executor.execute_plan(sample_plan, run_id="test-run")
        
        # Should have all 3 results
        assert len(results) == 3
        
        # First should be the loaded one
        assert results[0].content == "Already done"
        
        # Only 2 new executions
        assert executor.llm_client.create_completion.call_count == 2

    @pytest.mark.asyncio
    async def test_format_tools_builtin(self, executor):
        """Test formatting built-in tools."""
        tools = ["web_search", "code_interpreter"]
        formatted = executor._format_tools(tools)
        
        assert len(formatted) == 2
        assert formatted[0] == {"type": "web_search"}
        assert formatted[1] == {"type": "code_interpreter"}

    @pytest.mark.asyncio
    async def test_format_tools_custom_function(self, executor):
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
        assert formatted[0] == custom_tool

    @pytest.mark.asyncio
    async def test_format_tools_mcp(self, executor):
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

    @pytest.mark.asyncio
    async def test_build_messages_simple(self, executor):
        """Test building messages for a simple step."""
        step = Step(id="test", prompt="Do something")
        messages = executor._build_messages(step, {})
        
        assert len(messages) == 2
        assert messages[0]["role"] == "system"
        assert "You are executing step 'test'" in messages[0]["content"]
        assert messages[1]["role"] == "user"
        assert messages[1]["content"] == "Do something"

    @pytest.mark.asyncio
    async def test_build_messages_with_dependencies(self, executor):
        """Test building messages with dependency results."""
        step = Step(
            id="analyze",
            prompt="Analyze the data",
            dependencies=["fetch"],
        )
        
        previous_results = {
            "fetch": StepResult(
                step_id="fetch",
                status=StepStatus.COMPLETED,
                content="Data: [1, 2, 3]",
                attempt_count=1,
            )
        }
        
        messages = executor._build_messages(step, previous_results)
        
        # Should include dependency result in system message
        assert len(messages) == 2
        assert "Previous step results:" in messages[0]["content"]
        assert "fetch" in messages[0]["content"]
        assert "Data: [1, 2, 3]" in messages[0]["content"]

    @pytest.mark.asyncio
    async def test_build_messages_with_output_schema(self, executor):
        """Test building messages with output schema requirement."""
        output_schema = {
            "type": "object",
            "properties": {"result": {"type": "string"}},
        }
        
        step = Step(
            id="extract",
            prompt="Extract information",
            output_schema=output_schema,
        )
        
        messages = executor._build_messages(step, {})
        
        # Should include schema requirement in system message
        system_msg = messages[0]["content"]
        assert "must return a JSON object" in system_msg
        assert json.dumps(output_schema) in system_msg

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