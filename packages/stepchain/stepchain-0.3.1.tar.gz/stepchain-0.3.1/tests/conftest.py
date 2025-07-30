"""Pytest configuration and shared fixtures for StepChain tests."""

import asyncio
import json
from pathlib import Path
from typing import Any, AsyncGenerator, Generator
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from pydantic import BaseModel

from stepchain.core.models import Plan, Step, StepResult, StepStatus


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def sample_step() -> Step:
    """Create a sample step for testing."""
    return Step(
        id="test-step",
        prompt="Test prompt",
        description="Test description",
        dependencies=[],
        tools=["web_search"],
        output_schema=None,
    )


@pytest.fixture
def sample_plan() -> Plan:
    """Create a sample plan with multiple steps for testing."""
    return Plan(
        goal="Test goal",
        steps=[
            Step(
                id="step1",
                prompt="First step",
                description="First step description",
                dependencies=[],
                tools=[],
            ),
            Step(
                id="step2", 
                prompt="Second step",
                description="Second step description",
                dependencies=["step1"],
                tools=["web_search"],
            ),
            Step(
                id="step3",
                prompt="Third step",
                description="Third step description", 
                dependencies=["step1"],
                tools=[],
            ),
        ],
    )


@pytest.fixture
def sample_step_result() -> StepResult:
    """Create a sample step result for testing."""
    return StepResult(
        step_id="test-step",
        status=StepStatus.COMPLETED,
        content="Test content",
        error=None,
        attempt_count=1,
        output=None,
    )


@pytest.fixture
def mock_openai_client():
    """Create a mock OpenAI client."""
    mock_client = MagicMock()
    
    # Mock the Responses API (beta.responses.create)
    mock_response = MagicMock()
    mock_response.id = "resp_123"
    mock_response.output_text = "Test response"
    mock_response.content = [MagicMock(text="Test response")]
    
    mock_client.beta.responses.create = MagicMock(return_value=mock_response)
    
    return mock_client


@pytest.fixture
def mock_unified_llm_client():
    """Create a mock UnifiedLLMClient."""
    mock_instance = MagicMock()
    mock_instance.create_completion = MagicMock(
        return_value={
            "content": "Test response",
            "response_id": "resp_123",
            "usage": {"prompt_tokens": 10, "completion_tokens": 20},
        }
    )
    return mock_instance


@pytest.fixture
def temp_storage_dir(tmp_path: Path) -> Path:
    """Create a temporary directory for storage tests."""
    storage_dir = tmp_path / ".stepchain"
    storage_dir.mkdir()
    return storage_dir


@pytest.fixture
def mock_config(temp_storage_dir: Path):
    """Create a mock configuration."""
    from stepchain.config import Config
    
    return Config(
        storage_path=temp_storage_dir,
        log_level="DEBUG",
        llm_model="gpt-4",
        max_retries=3,
        base_delay=1.0,
        max_delay=60.0,
        timeout_seconds=300,
    )


@pytest.fixture
def mock_executor(mock_unified_llm_client, temp_storage_dir):
    """Create a mock executor with dependencies."""
    from stepchain.core.executor import Executor
    from stepchain.storage.jsonl import JSONLStore
    
    mock_store = MagicMock(spec=JSONLStore)
    executor = Executor(client=mock_unified_llm_client, store=mock_store)
    return executor


@pytest.fixture
def sample_tool_definition() -> dict[str, Any]:
    """Create a sample tool definition."""
    return {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Search the web for information",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query",
                    }
                },
                "required": ["query"],
            },
        },
    }


@pytest.fixture
def sample_mcp_tool() -> dict[str, Any]:
    """Create a sample MCP tool configuration."""
    return {
        "type": "mcp",
        "server_label": "test_server",
        "server_url": "http://localhost:3000",
        "allowed_tools": ["search", "fetch"],
    }


class MockOutputSchema(BaseModel):
    """Mock output schema for testing."""
    
    result: str
    confidence: float


@pytest.fixture
def sample_output_schema():
    """Return a sample output schema class."""
    return MockOutputSchema