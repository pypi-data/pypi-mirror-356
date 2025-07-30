"""Unit tests for TaskDecomposer."""

import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from stepchain.core.decomposer import DecompositionStrategy, TaskDecomposer
from stepchain.core.models import Plan, Step


class TestTaskDecomposer:
    """Test cases for TaskDecomposer."""

    @pytest.fixture
    def decomposer(self, mock_config):
        """Create a TaskDecomposer instance for testing."""
        with patch("stepchain.decomposer.UnifiedLLMClient"):
            return TaskDecomposer(
                strategy=DecompositionStrategy.THOROUGH,
                config=mock_config,
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

    @pytest.mark.asyncio
    async def test_decompose_simple_task(self, decomposer, mock_llm_response):
        """Test decomposing a simple task."""
        # Mock the LLM client
        decomposer.llm_client.create_completion = AsyncMock(return_value=mock_llm_response)
        
        # Decompose task
        plan = await decomposer.decompose("Analyze customer feedback")
        
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

    @pytest.mark.asyncio
    async def test_decompose_with_tools(self, decomposer):
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
        
        decomposer.llm_client.create_completion = AsyncMock(return_value=mock_response)
        
        # Define available tools
        tools = ["web_search", "code_interpreter"]
        
        plan = await decomposer.decompose("Research market trends", tools=tools)
        
        assert len(plan.steps) == 2
        assert plan.steps[0].tools == ["web_search"]
        assert plan.steps[1].tools == ["code_interpreter"]

    @pytest.mark.asyncio
    async def test_decompose_with_output_schema(self, decomposer):
        """Test decomposing with output schema requirement."""
        mock_response = {
            "content": json.dumps({
                "goal": "Extract product data",
                "steps": [
                    {
                        "id": "extract-data",
                        "prompt": "Extract product information",
                        "dependencies": [],
                        "tools": [],
                        "output_schema": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "price": {"type": "number"},
                            },
                        },
                    },
                ]
            })
        }
        
        decomposer.llm_client.create_completion = AsyncMock(return_value=mock_response)
        
        output_schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "price": {"type": "number"},
            },
        }
        
        plan = await decomposer.decompose(
            "Extract product data",
            output_schema=output_schema,
        )
        
        assert plan.steps[0].output_schema == output_schema

    @pytest.mark.asyncio
    async def test_decompose_thorough_strategy(self, mock_config):
        """Test thorough decomposition strategy."""
        with patch("stepchain.decomposer.UnifiedLLMClient") as mock_client:
            decomposer = TaskDecomposer(
                strategy=DecompositionStrategy.THOROUGH,
                config=mock_config,
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
            
            decomposer.llm_client.create_completion = AsyncMock(return_value=mock_response)
            
            plan = await decomposer.decompose("Complex analysis")
            
            # Thorough strategy should produce more steps
            assert len(plan.steps) == 10

    @pytest.mark.asyncio
    async def test_decompose_quick_strategy(self, mock_config):
        """Test quick decomposition strategy."""
        with patch("stepchain.decomposer.UnifiedLLMClient") as mock_client:
            decomposer = TaskDecomposer(
                strategy=DecompositionStrategy.QUICK,
                config=mock_config,
            )
            
            mock_response = {
                "content": json.dumps({
                    "goal": "Simple task",
                    "steps": [
                        {"id": "step1", "prompt": "Do everything", "dependencies": []},
                    ]
                })
            }
            
            decomposer.llm_client.create_completion = AsyncMock(return_value=mock_response)
            
            plan = await decomposer.decompose("Simple task")
            
            # Quick strategy should produce fewer steps
            assert len(plan.steps) == 1

    @pytest.mark.asyncio
    async def test_decompose_invalid_response(self, decomposer):
        """Test handling invalid LLM response."""
        # Mock invalid JSON response
        decomposer.llm_client.create_completion = AsyncMock(
            return_value={"content": "Not valid JSON"}
        )
        
        with pytest.raises(ValueError, match="Failed to parse plan"):
            await decomposer.decompose("Test task")

    @pytest.mark.asyncio
    async def test_decompose_missing_fields(self, decomposer):
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
        
        decomposer.llm_client.create_completion = AsyncMock(return_value=mock_response)
        
        with pytest.raises(ValueError):
            await decomposer.decompose("Test task")

    @pytest.mark.asyncio
    async def test_map_tools_to_definitions(self, decomposer):
        """Test mapping tool names to definitions."""
        # Test with built-in tools
        tools = ["web_search", "code_interpreter"]
        definitions = decomposer._map_tools_to_definitions(tools)
        
        assert len(definitions) == 2
        assert definitions[0]["type"] == "web_search"
        assert definitions[1]["type"] == "code_interpreter"
        
        # Test with custom tool
        custom_tool = {
            "type": "function",
            "function": {
                "name": "custom_func",
                "description": "Custom function",
                "parameters": {},
            }
        }
        
        tools_with_custom = ["web_search", custom_tool]
        definitions = decomposer._map_tools_to_definitions(tools_with_custom)
        
        assert len(definitions) == 2
        assert definitions[0]["type"] == "web_search"
        assert definitions[1]["type"] == "function"

    @pytest.mark.asyncio
    async def test_decompose_with_examples(self, decomposer):
        """Test decomposition with example steps provided."""
        mock_response = {
            "content": json.dumps({
                "goal": "Test with examples",
                "steps": [
                    {"id": "step1", "prompt": "First step", "dependencies": []},
                    {"id": "step2", "prompt": "Second step", "dependencies": ["step1"]},
                ]
            })
        }
        
        decomposer.llm_client.create_completion = AsyncMock(return_value=mock_response)
        
        examples = [
            Step(id="example1", prompt="Example step 1"),
            Step(id="example2", prompt="Example step 2", dependencies=["example1"]),
        ]
        
        plan = await decomposer.decompose(
            "Test with examples",
            examples=examples,
        )
        
        # Verify the plan was created (examples influence prompt but not output structure)
        assert isinstance(plan, Plan)
        assert len(plan.steps) == 2

    def test_get_strategy_guidelines(self, decomposer):
        """Test strategy guidelines generation."""
        # Test THOROUGH strategy
        decomposer.strategy = DecompositionStrategy.THOROUGH
        guidelines = decomposer._get_strategy_guidelines()
        assert "comprehensive" in guidelines.lower()
        assert "detailed" in guidelines.lower()
        
        # Test QUICK strategy
        decomposer.strategy = DecompositionStrategy.QUICK
        guidelines = decomposer._get_strategy_guidelines()
        assert "minimal" in guidelines.lower()
        assert "high-level" in guidelines.lower()
        
        # Test BALANCED strategy
        decomposer.strategy = DecompositionStrategy.BALANCED
        guidelines = decomposer._get_strategy_guidelines()
        assert "moderate" in guidelines.lower()
        assert "balance" in guidelines.lower()