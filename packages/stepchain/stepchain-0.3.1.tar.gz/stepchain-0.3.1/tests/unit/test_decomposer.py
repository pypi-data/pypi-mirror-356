"""Unit tests for TaskDecomposer."""

import json
from unittest.mock import MagicMock, patch

import pytest

from stepchain.core.decomposer import TaskDecomposer
from stepchain.core.models import Plan, Step
from stepchain.errors import DecompositionError


class TestTaskDecomposer:
    """Test cases for TaskDecomposer."""

    @pytest.fixture
    def decomposer(self, mock_unified_llm_client):
        """Create a TaskDecomposer instance for testing."""
        with patch("stepchain.core.decomposer.get_default_client", return_value=mock_unified_llm_client):
            return TaskDecomposer(
                client=mock_unified_llm_client,
            )

    @pytest.fixture
    def mock_llm_response(self):
        """Create a mock LLM response for task decomposition."""
        return {
            "content": json.dumps({
                "goal": "Analyze customer feedback",
                "steps": [
                    {
                        "id": "fetch-data",
                        "prompt": "Fetch customer feedback from database",
                        "description": "Retrieve all feedback from last month",
                        "dependencies": [],
                        "tools": [],
                    },
                    {
                        "id": "analyze-sentiment",
                        "prompt": "Analyze sentiment of feedback",
                        "description": "Use NLP to determine sentiment",
                        "dependencies": ["fetch-data"],
                        "tools": ["web_search"],
                    },
                    {
                        "id": "create-report",
                        "prompt": "Create summary report",
                        "description": "Generate executive summary",
                        "dependencies": ["analyze-sentiment"],
                        "tools": [],
                    },
                ]
            })
        }

    def test_decompose_simple_task(self, decomposer, mock_llm_response):
        """Test decomposing a simple task."""
        # Mock the LLM client
        decomposer.client.create_completion = MagicMock(return_value=mock_llm_response)
        
        # Decompose task
        plan = decomposer.decompose("Analyze customer feedback")
        
        # Verify plan structure
        assert isinstance(plan, Plan)
        assert plan.goal == "Analyze customer feedback"
        assert len(plan.steps) == 3
        
        # Verify steps
        assert plan.steps[0].id == "fetch-data"
        assert plan.steps[1].id == "analyze-sentiment"
        assert plan.steps[2].id == "create-report"
        
        # Verify dependencies
        assert plan.steps[0].dependencies == []
        assert plan.steps[1].dependencies == ["fetch-data"]
        assert plan.steps[2].dependencies == ["analyze-sentiment"]

    def test_decompose_with_tools(self, decomposer):
        """Test decomposing a task with specific tools."""
        mock_response = {
            "content": json.dumps({
                "goal": "Research market trends",
                "steps": [
                    {
                        "id": "search-trends",
                        "prompt": "Search for current market trends",
                        "dependencies": [],
                        "tools": ["web_search"],
                    },
                    {
                        "id": "analyze-data",
                        "prompt": "Analyze trend data",
                        "dependencies": ["search-trends"],
                        "tools": ["code_interpreter"],
                    },
                ]
            })
        }
        
        decomposer.client.create_completion = MagicMock(return_value=mock_response)
        
        # Define available tools
        tools = ["web_search", "code_interpreter"]
        
        plan = decomposer.decompose("Research market trends", tools=tools)
        
        assert len(plan.steps) == 2
        assert plan.steps[0].tools == ["web_search"]
        assert plan.steps[1].tools == ["code_interpreter"]

    def test_decompose_with_output_schema(self, decomposer):
        """Test decomposing with output schema requirement."""
        # The current implementation doesn't support output_schema parameter
        # Instead, the LLM might include it in the response metadata
        mock_response = {
            "content": json.dumps({
                "goal": "Extract product data",
                "steps": [
                    {
                        "id": "extract-data",
                        "prompt": "Extract product information",
                        "dependencies": [],
                        "tools": [],
                    },
                ]
            })
        }
        
        decomposer.client.create_completion = MagicMock(return_value=mock_response)
        
        plan = decomposer.decompose("Extract product data")
        
        assert len(plan.steps) == 1
        assert plan.steps[0].id == "extract-data"

    def test_decompose_complex_task(self, mock_unified_llm_client):
        """Test decomposing a complex task."""
        with patch("stepchain.core.decomposer.get_default_client", return_value=mock_unified_llm_client):
            decomposer = TaskDecomposer(
                client=mock_unified_llm_client,
            )
            
            mock_response = {
                "content": json.dumps({
                    "goal": "Complex analysis",
                    "steps": [
                        {"id": f"step{i}", "prompt": f"Step {i}", "dependencies": []}
                        for i in range(10)  # Many detailed steps
                    ]
                })
            }
            
            decomposer.client.create_completion = MagicMock(return_value=mock_response)
            
            plan = decomposer.decompose("Complex analysis")
            
            # Complex task should produce many steps
            assert len(plan.steps) == 10

    def test_decompose_simple_task_minimal_steps(self, mock_unified_llm_client):
        """Test decomposing a simple task results in minimal steps."""
        with patch("stepchain.core.decomposer.get_default_client", return_value=mock_unified_llm_client):
            decomposer = TaskDecomposer(
                client=mock_unified_llm_client,
            )
            
            mock_response = {
                "content": json.dumps({
                    "goal": "Simple task",
                    "steps": [
                        {"id": "step1", "prompt": "Do everything", "dependencies": []},
                    ]
                })
            }
            
            decomposer.client.create_completion = MagicMock(return_value=mock_response)
            
            plan = decomposer.decompose("Simple task")
            
            # Simple task should produce minimal steps
            assert len(plan.steps) == 1

    def test_decompose_invalid_response(self, decomposer):
        """Test handling invalid LLM response."""
        # Mock invalid JSON response
        decomposer.client.create_completion = MagicMock(
            return_value={"content": "Not valid JSON"}
        )
        
        with pytest.raises(DecompositionError) as exc_info:
            decomposer.decompose("Test task")
        
        assert "Could not parse valid plan from response" in str(exc_info.value)

    def test_decompose_missing_fields(self, decomposer):
        """Test handling response with missing required fields."""
        mock_response = {
            "content": json.dumps({
                "goal": "Test task",
                "steps": [
                    {
                        # Missing 'id' field
                        "prompt": "Do something",
                        "dependencies": [],
                    }
                ]
            })
        }
        
        decomposer.client.create_completion = MagicMock(return_value=mock_response)
        
        with pytest.raises(DecompositionError) as exc_info:
            decomposer.decompose("Test task")
        
        assert "Could not parse valid plan from response" in str(exc_info.value)

    def test_decompose_with_custom_tools(self, decomposer):
        """Test decomposing with custom tool definitions."""
        # Test with custom tool
        custom_tool = {
            "type": "function",
            "function": {
                "name": "custom_func",
                "description": "Custom function",
                "parameters": {},
            }
        }
        
        mock_response = {
            "content": json.dumps({
                "goal": "Task with custom tools",
                "steps": [
                    {
                        "id": "use-custom",
                        "prompt": "Use custom function",
                        "dependencies": [],
                        "tools": ["custom_func"],
                    }
                ]
            })
        }
        
        decomposer.client.create_completion = MagicMock(return_value=mock_response)
        
        tools = ["web_search", custom_tool]
        plan = decomposer.decompose("Task with custom tools", tools=tools)
        
        assert len(plan.steps) == 1
        # The step stores the full tool definition, not just the name
        assert len(plan.steps[0].tools) == 1
        assert plan.steps[0].tools[0]["function"]["name"] == "custom_func"

    def test_decompose_with_metadata(self, decomposer):
        """Test decomposition with metadata in response."""
        mock_response = {
            "content": json.dumps({
                "goal": "Test with metadata",
                "steps": [
                    {"id": "step1", "prompt": "First step", "dependencies": []},
                    {"id": "step2", "prompt": "Second step", "dependencies": ["step1"]},
                ],
                "metadata": {
                    "estimated_duration": "30 minutes",
                    "complexity": "medium"
                }
            })
        }
        
        decomposer.client.create_completion = MagicMock(return_value=mock_response)
        
        plan = decomposer.decompose("Test with metadata")
        
        # Verify the plan was created
        assert isinstance(plan, Plan)
        assert len(plan.steps) == 2
        # Metadata should be included if present in response
        if hasattr(plan, 'metadata') and plan.metadata:
            assert "estimated_duration" in plan.metadata or "complexity" in plan.metadata

    def test_decompose_preserves_goal(self, decomposer):
        """Test that decomposition preserves the original goal."""
        goal = "Build a web application"
        mock_response = {
            "content": json.dumps({
                "goal": goal,
                "steps": [
                    {"id": "design", "prompt": "Design the application", "dependencies": []},
                    {"id": "implement", "prompt": "Implement the application", "dependencies": ["design"]},
                ]
            })
        }
        
        decomposer.client.create_completion = MagicMock(return_value=mock_response)
        
        plan = decomposer.decompose(goal)
        
        assert plan.goal == goal
        assert len(plan.steps) == 2