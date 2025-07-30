"""Data models for StepChain.

This module defines the core data structures used throughout the SDK.
"""

import re
from datetime import UTC, datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class StepStatus(str, Enum):
    """Status of a step execution."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"
    SKIPPED = "skipped"


class ErrorType(str, Enum):
    """Classification of errors for retry strategies."""

    RATE_LIMIT = "rate_limit"
    SERVER_ERROR = "server_error"
    NETWORK = "network"
    TOOL_ERROR = "tool_error"
    USER_ERROR = "user_error"
    OTHER = "other"
    UNKNOWN = "unknown"


class Step(BaseModel):
    """Represents a single step in an execution plan.

    Example:
        >>> step = Step(
        ...     id="analyze",
        ...     prompt="Analyze the data",
        ...     tools=["python", "calculator"],
        ...     dependencies=["fetch_data"],
        ...     max_retries=3
        ... )
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: str = Field(..., description="Unique identifier for the step")
    prompt: str = Field(..., description="The prompt to send to the LLM")
    description: str | None = Field(default=None, description="Human-readable description")
    tools: list[str | dict[str, Any]] = Field(
        default_factory=list,
        description="Tools: built-in names (str) or MCP/function configs (dict)"
    )
    dependencies: list[str] = Field(default_factory=list, description="Step IDs this depends on")
    output_schema: dict[str, Any] | None = Field(default=None, description="Expected output schema")
    max_retries: int = Field(default=3, description="Maximum retry attempts")
    timeout: float | None = Field(default=None, description="Timeout in seconds")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    @field_validator('id')
    @classmethod
    def validate_id(cls, v: str) -> str:
        """Validate step ID format."""
        if not v or not v.strip():
            raise ValueError("Step ID cannot be empty")
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError(
                "Step ID must contain only alphanumeric characters, underscores, and hyphens"
            )
        return v
    
    @field_validator('tools')
    @classmethod
    def validate_tool_names(cls, v: list[str | dict[str, Any]]) -> list[str | dict[str, Any]]:
        """Validate tools - can be strings (built-in) or dicts (MCP/functions)."""
        for tool in v:
            if isinstance(tool, str):
                # Validate built-in tool names
                if not re.match(r'^[a-zA-Z0-9_-]+$', tool):
                    raise ValueError(f"Tool name '{tool}' contains invalid characters")
                if len(tool) > 50:
                    raise ValueError(f"Tool name '{tool}' is too long (max 50 characters)")
            elif isinstance(tool, dict):
                # Validate dict tools have required fields
                if "type" not in tool:
                    raise ValueError("Tool dict must have 'type' field")
                if tool["type"] == "mcp":
                    if "server_label" not in tool or "server_url" not in tool:
                        raise ValueError("MCP tool must have 'server_label' and 'server_url'")
                elif tool["type"] == "function" and (
                    "function" not in tool or "name" not in tool.get("function", {})
                ):
                    raise ValueError("Function tool must have function.name")
            else:
                raise ValueError(f"Tool must be string or dict, got {type(tool)}")
        return v
    
    @field_validator('prompt')
    @classmethod
    def validate_prompt(cls, v: str) -> str:
        """Validate prompt is not empty."""
        if not v or not v.strip():
            raise ValueError("Prompt cannot be empty")
        return v.strip()


class Plan(BaseModel):
    """Execution plan containing multiple steps.

    Example:
        >>> plan = Plan(
        ...     goal="Process data from API and generate report",
        ...     id="data-pipeline",
        ...     steps=[
        ...         Step(id="fetch", prompt="Fetch data from API"),
        ...         Step(id="process", prompt="Process the data", dependencies=["fetch"])
        ...     ]
        ... )
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: str = Field(default="default", description="Plan identifier")
    goal: str = Field(..., description="Goal or objective of the plan")
    steps: list[Step] = Field(..., description="List of steps to execute")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

    @field_validator('steps')
    @classmethod
    def validate_unique_ids(cls, v: list[Step]) -> list[Step]:
        """Validate that all step IDs are unique."""
        step_ids = [step.id for step in v]
        if len(step_ids) != len(set(step_ids)):
            raise ValueError("Duplicate step IDs found")
        return v
    
    def model_post_init(self, __context: Any) -> None:
        """Validate dependencies after model creation."""
        self.validate_dependencies()
        self.validate_no_circular_dependencies()
    
    def validate_dependencies(self) -> None:
        """Validate that all dependencies reference existing steps."""
        step_ids = {step.id for step in self.steps}
        for step in self.steps:
            for dep in step.dependencies:
                if dep not in step_ids:
                    raise ValueError(f"Step '{step.id}' depends on non-existent step '{dep}'")
    
    def validate_no_circular_dependencies(self) -> None:
        """Validate that there are no circular dependencies."""
        from collections import defaultdict
        
        # Build adjacency list
        graph = defaultdict(list)
        for step in self.steps:
            for dep in step.dependencies:
                graph[dep].append(step.id)
        
        # DFS to detect cycles
        visited = set()
        rec_stack = set()
        
        def has_cycle(node: str) -> bool:
            visited.add(node)
            rec_stack.add(node)
            
            for neighbor in graph[node]:
                if neighbor not in visited:
                    if has_cycle(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True
            
            rec_stack.remove(node)
            return False
        
        for step in self.steps:
            if step.id not in visited and has_cycle(step.id):
                raise ValueError("Circular dependency detected")
    
    def get_execution_order(self) -> list[str]:
        """Get topologically sorted execution order."""
        from collections import defaultdict, deque
        
        # Build in-degree map
        in_degree = defaultdict(int)
        graph = defaultdict(list)
        
        for step in self.steps:
            if step.id not in in_degree:
                in_degree[step.id] = 0
            for dep in step.dependencies:
                graph[dep].append(step.id)
                in_degree[step.id] += 1
        
        # Topological sort using Kahn's algorithm
        queue = deque([step.id for step in self.steps if in_degree[step.id] == 0])
        result = []
        
        while queue:
            node = queue.popleft()
            result.append(node)
            
            for neighbor in graph[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        return result
    
    def get_step_dependencies(self) -> dict[str, list[str]]:
        """Get a mapping of step IDs to their dependencies."""
        return {step.id: step.dependencies for step in self.steps}


class StepResult(BaseModel):
    """Result of executing a single step.

    Example:
        >>> result = StepResult(
        ...     step_id="analyze",
        ...     status=StepStatus.COMPLETED,
        ...     response_id="resp_123",
        ...     output={"analysis": "Data shows positive trend"},
        ...     attempt_count=1
        ... )
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)

    step_id: str = Field(..., description="ID of the executed step")
    status: StepStatus = Field(..., description="Current status")
    content: str | None = Field(default=None, description="Text content of the result")
    response_id: str | None = Field(default=None, description="OpenAI response ID")
    previous_response_id: str | None = Field(default=None, description="Previous response ID")
    output: dict[str, Any] | None = Field(
        default=None, description="Structured output if schema was provided"
    )
    tool_calls: list[dict[str, Any]] | None = Field(
        default=None, description="Tool calls made in this step"
    )
    error: str | None = Field(default=None, description="Error message if failed")
    error_type: ErrorType | None = Field(default=None, description="Type of error")
    attempt_count: int = Field(default=1, description="Number of attempts made")
    started_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    completed_at: datetime | None = Field(default=None)
    duration_seconds: float | None = Field(default=None)
    metadata: dict[str, Any] = Field(default_factory=dict)

    def calculate_duration(self) -> None:
        """Calculate and set duration if completed."""
        if self.completed_at and self.started_at:
            self.duration_seconds = (self.completed_at - self.started_at).total_seconds()


class StepExecutionState(BaseModel):
    """State of a single step during execution."""
    
    step_id: str
    status: StepStatus
    result: StepResult | None = None
    started_at: datetime | None = None
    updated_at: datetime | None = None


class ExecutionState(BaseModel):
    """Complete state of a plan execution."""
    
    run_id: str
    plan: Plan
    status: str  # "pending", "running", "completed", "failed"
    started_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    completed_at: datetime | None = None
    completed_steps: list[str] = Field(default_factory=list)
    step_states: dict[str, StepExecutionState] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)
