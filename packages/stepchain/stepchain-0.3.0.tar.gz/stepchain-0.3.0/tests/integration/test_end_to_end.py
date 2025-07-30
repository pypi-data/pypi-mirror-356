"""End-to-end integration tests for StepChain."""

import asyncio
import json
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from stepchain import (
    AsyncExecutor,
    Config,
    DecompositionStrategy,
    Executor,
    JSONLStore,
    Plan,
    Step,
    StepResult,
    StepStatus,
    TaskDecomposer,
    setup_stepchain,
)
from stepchain.core.models import ExecutionState


class TestEndToEnd:
    """End-to-end integration tests."""

    @pytest.fixture
    def config(self, temp_storage_dir):
        """Create test configuration."""
        return Config(
            storage_path=temp_storage_dir,
            log_level="DEBUG",
            llm_model="gpt-4",
            max_retries=2,
            timeout_seconds=60,
        )

    @pytest.mark.asyncio
    async def test_full_workflow_simple_task(self, config, temp_storage_dir):
        """Test complete workflow from decomposition to execution."""
        # Create mock client
        mock_client = MagicMock()
        
        # Create mock store
        mock_store = MagicMock()
        mock_store.get_results.return_value = []  # No previous results
        mock_store.save_plan = MagicMock()
        mock_store.save_result = MagicMock()
        
        with patch("stepchain.core.decomposer.get_default_client", return_value=mock_client), \
             patch("stepchain.core.executor.get_default_client", return_value=mock_client), \
             patch("stepchain.core.executor.JSONLStore", return_value=mock_store):
            
            # Mock decomposer response for first call, then executor responses
            mock_client.create_completion = MagicMock(
                side_effect=[
                    # Decomposer response
                    {
                        "content": json.dumps({
                            "goal": "Write a hello world program",
                            "steps": [
                                {
                                    "id": "write-code",
                                    "prompt": "Write a Python hello world program",
                                    "dependencies": [],
                                    "tools": [],
                                },
                                {
                                    "id": "test-code",
                                    "prompt": "Test the hello world program",
                                    "dependencies": ["write-code"],
                                    "tools": [],
                                },
                            ]
                        })
                    },
                    # Executor responses
                    {
                        "content": 'print("Hello, World!")',
                        "response_id": "resp_1",
                    },
                    {
                        "content": "Code tested successfully. Output: Hello, World!",
                        "response_id": "resp_2",
                    },
                ]
            )
            
            # Decompose task
            decomposer = TaskDecomposer()
            plan = decomposer.decompose("Write and test a hello world program")
            
            assert len(plan.steps) == 2
            
            # Execute plan
            executor = Executor()
            results = executor.execute_plan(plan, run_id="test-run")
            assert len(results) == 2
            assert all(r.status == StepStatus.COMPLETED for r in results)
            assert 'print("Hello, World!")' in results[0].content
            assert "tested successfully" in results[1].content

    @pytest.mark.asyncio
    async def test_workflow_with_failure_and_resume(self, config, temp_storage_dir):
        """Test workflow with failure and resume capability."""
        plan = Plan(
            goal="Multi-step task",
            steps=[
                Step(id="step1", prompt="First step"),
                Step(id="step2", prompt="Second step", dependencies=["step1"]),
                Step(id="step3", prompt="Third step", dependencies=["step2"]),
            ]
        )
        
        # Create mock client
        mock_client = MagicMock()
        
        with patch("stepchain.core.executor.get_default_client", return_value=mock_client):
            # First execution - fails at step 2
            mock_client.create_completion = MagicMock(
                side_effect=[
                    {"content": "Step 1 done", "response_id": "resp_1"},
                    Exception("Network error"),
                ]
            )
            
            executor = Executor(store=JSONLStore(base_path=temp_storage_dir))
            
            with pytest.raises(Exception):
                executor.execute_plan(plan, run_id="resume-test")
            
            # Check that step 1 was saved and step 2 failed
            store = JSONLStore(base_path=temp_storage_dir)
            saved_results = store.get_results("resume-test")
            assert len(saved_results) == 2
            assert saved_results[0].step_id == "step1"
            assert saved_results[0].status == StepStatus.COMPLETED
            assert saved_results[1].step_id == "step2"
            assert saved_results[1].status == StepStatus.FAILED
            
            # Resume execution - complete remaining steps
            mock_client.create_completion = MagicMock(
                side_effect=[
                    {"content": "Step 2 done", "response_id": "resp_2"},
                    {"content": "Step 3 done", "response_id": "resp_3"},
                ]
            )
            
            # Execute again - should resume from step 2
            results = executor.execute_plan(plan, run_id="resume-test")
            
            # Only steps 2 and 3 should be executed (step 1 was already completed)
            assert len(results) == 2
            assert results[0].content == "Step 2 done"
            assert results[1].content == "Step 3 done"

    @pytest.mark.asyncio
    async def test_workflow_with_tools(self, config):
        """Test workflow with tool usage."""
        plan = Plan(
            goal="Search and analyze",
            steps=[
                Step(
                    id="search",
                    prompt="Search for Python best practices",
                    tools=["web_search"],
                ),
                Step(
                    id="analyze",
                    prompt="Analyze the search results",
                    dependencies=["search"],
                ),
            ]
        )
        
        # Create mock client
        mock_client = MagicMock()
        
        # Create mock store
        mock_store = MagicMock()
        mock_store.get_results.return_value = []
        mock_store.save_plan = MagicMock()
        mock_store.save_result = MagicMock()
        
        with patch("stepchain.core.executor.get_default_client", return_value=mock_client), \
             patch("stepchain.core.executor.JSONLStore", return_value=mock_store):
            mock_client.create_completion = MagicMock(
                side_effect=[
                    {
                        "content": "Found 10 best practices for Python",
                        "response_id": "resp_1",
                    },
                    {
                        "content": "Analysis complete: Use type hints, follow PEP8...",
                        "response_id": "resp_2",
                    },
                ]
            )
            
            executor = Executor()
            results = executor.execute_plan(plan, run_id="tools-test")
            
            # Verify tools were passed correctly
            first_call = mock_client.create_completion.call_args_list[0]
            assert "tools" in first_call.kwargs
            assert first_call.kwargs["tools"][0]["type"] == "web_search"

    @pytest.mark.asyncio
    async def test_async_executor_parallel_execution(self, config):
        """Test AsyncExecutor with parallel step execution."""
        plan = Plan(
            goal="Parallel processing",
            steps=[
                Step(id="setup", prompt="Setup environment"),
                Step(id="task1", prompt="Process dataset 1", dependencies=["setup"]),
                Step(id="task2", prompt="Process dataset 2", dependencies=["setup"]),
                Step(id="task3", prompt="Process dataset 3", dependencies=["setup"]),
                Step(
                    id="combine",
                    prompt="Combine results",
                    dependencies=["task1", "task2", "task3"],
                ),
            ]
        )
        
        execution_order = []
        
        async def mock_completion(**kwargs):
            # Extract step info from the prompt
            prompt = kwargs.get("messages", [{}])[-1].get("content", "")
            step_name = prompt.split()[-1]
            execution_order.append(step_name)
            
            # Simulate some processing time
            await asyncio.sleep(0.1)
            
            return {
                "content": f"Completed: {prompt}",
                "response_id": f"resp_{len(execution_order)}",
            }
        
        with patch("stepchain.core.executor.UnifiedLLMClient") as mock_client:
            mock_client.return_value.create_completion = AsyncMock(
                side_effect=mock_completion
            )
            
            async_executor = AsyncExecutor()
            results = await async_executor.execute_plan(plan, run_id="async-test")
            
            assert len(results) == 5
            assert all(r.status == StepStatus.COMPLETED for r in results)
            
            # Verify execution order
            assert execution_order[0] == "environment"  # Setup first
            
            # task1, task2, task3 should execute in parallel (order may vary)
            parallel_tasks = set(execution_order[1:4])
            assert parallel_tasks == {"1", "2", "3"}
            
            # Combine should be last
            assert execution_order[4] == "results"

    @pytest.mark.asyncio
    async def test_workflow_with_output_schema(self, config):
        """Test workflow with structured output validation."""
        output_schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "number"},
                "email": {"type": "string"},
            },
            "required": ["name", "age"],
        }
        
        plan = Plan(
            goal="Extract user data",
            steps=[
                Step(
                    id="extract",
                    prompt="Extract user information from text",
                    output_schema=output_schema,
                ),
            ]
        )
        
        with patch("stepchain.core.executor.UnifiedLLMClient") as mock_client:
            mock_client.return_value.create_completion = AsyncMock(
                return_value={
                    "content": json.dumps({
                        "name": "John Doe",
                        "age": 30,
                        "email": "john@example.com",
                    }),
                    "response_id": "resp_1",
                }
            )
            
            executor = Executor()
            results = executor.execute_plan(plan, run_id="schema-test")
            
            assert len(results) == 1
            assert results[0].status == StepStatus.COMPLETED
            assert results[0].output == {
                "name": "John Doe",
                "age": 30,
                "email": "john@example.com",
            }

    @pytest.mark.asyncio
    async def test_quick_start_function(self, temp_storage_dir):
        """Test the quick_start convenience function."""
        with patch("stepchain.decomposer.UnifiedLLMClient") as mock_decomposer, \
             patch("stepchain.core.executor.UnifiedLLMClient") as mock_executor, \
             patch("stepchain.config.get_storage_path", return_value=temp_storage_dir):
            
            # Mock decomposition
            mock_decomposer.return_value.create_completion = AsyncMock(
                return_value={
                    "content": json.dumps({
                        "goal": "Simple task",
                        "steps": [
                            {
                                "id": "do-task",
                                "prompt": "Complete the simple task",
                                "dependencies": [],
                            }
                        ]
                    })
                }
            )
            
            # Mock execution
            mock_executor.return_value.create_completion = AsyncMock(
                return_value={
                    "content": "Task completed successfully",
                    "response_id": "resp_1",
                }
            )
            
            # Import and use quick_start
            from stepchain import quick_start
            
            result = await quick_start("Do a simple task")
            
            assert result is not None
            assert isinstance(result, StepResult)
            assert result.status == StepStatus.COMPLETED
            assert "completed successfully" in result.content

    def test_setup_stepchain(self, temp_storage_dir):
        """Test the setup_stepchain initialization function."""
        with patch("stepchain.config.get_storage_path", return_value=temp_storage_dir):
            config = setup_stepchain(log_level="INFO")
            
            assert isinstance(config, Config)
            assert config.log_level == "INFO"
            assert config.storage_path == temp_storage_dir
            
            # Check that storage directory was created
            assert temp_storage_dir.exists()

    @pytest.mark.asyncio
    async def test_complex_dependency_graph(self, config):
        """Test execution with complex dependency graph."""
        # Create a diamond-shaped dependency graph
        plan = Plan(
            goal="Complex dependencies",
            steps=[
                Step(id="start", prompt="Initialize"),
                Step(id="branch1", prompt="Process branch 1", dependencies=["start"]),
                Step(id="branch2", prompt="Process branch 2", dependencies=["start"]),
                Step(
                    id="merge",
                    prompt="Merge branches",
                    dependencies=["branch1", "branch2"],
                ),
                Step(id="finalize", prompt="Finalize", dependencies=["merge"]),
            ]
        )
        
        executed_steps = []
        
        async def track_execution(**kwargs):
            prompt = kwargs.get("messages", [{}])[-1].get("content", "")
            for step in plan.steps:
                if step.prompt == prompt:
                    executed_steps.append(step.id)
                    break
            
            return {
                "content": f"Completed: {prompt}",
                "response_id": f"resp_{len(executed_steps)}",
            }
        
        with patch("stepchain.core.executor.UnifiedLLMClient") as mock_client:
            mock_client.return_value.create_completion = AsyncMock(
                side_effect=track_execution
            )
            
            executor = Executor()
            results = executor.execute_plan(plan, run_id="complex-deps")
            
            assert len(results) == 5
            
            # Verify dependency order
            assert executed_steps.index("start") < executed_steps.index("branch1")
            assert executed_steps.index("start") < executed_steps.index("branch2")
            assert executed_steps.index("branch1") < executed_steps.index("merge")
            assert executed_steps.index("branch2") < executed_steps.index("merge")
            assert executed_steps.index("merge") < executed_steps.index("finalize")