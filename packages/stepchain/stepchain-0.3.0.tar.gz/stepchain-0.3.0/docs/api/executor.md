# Executor API Reference

The executor module provides the main execution logic with retry handling.

## Executor

Synchronous executor for running plans with OpenAI Responses API.

### Constructor

```python
Executor(
    client: Optional[LLMClient] = None,
    store: Optional[AbstractStore] = None,
    compression_strategy: Optional[CompressionStrategy] = None,
    telemetry: Optional[Telemetry] = None
)
```

**Parameters:**
- `client`: LLM client (defaults to OpenAI)
- `store`: Storage backend (defaults to JSONLStore)
- `compression_strategy`: History compression (defaults to FullHistory)
- `telemetry`: Telemetry instance

### Methods

#### execute_plan

Execute a plan, optionally resuming from previous run.

```python
execute_plan(
    plan: Plan,
    run_id: str,
    resume: bool = True
) -> list[StepResult]
```

**Parameters:**
- `plan`: The execution plan
- `run_id`: Unique identifier for this run
- `resume`: Whether to resume from previous results

**Returns:** List of step results

**Example:**
```python
from stepchain import Executor, Plan, Step

executor = Executor()
plan = Plan(
    goal="Fetch and process data from external API",
    steps=[
        Step(id="fetch", prompt="Fetch data from API"),
        Step(id="process", prompt="Process the data", dependencies=["fetch"])
    ]
)

results = executor.execute_plan(plan, run_id="analysis_20240115")
```

## AsyncExecutor

Asynchronous executor with concurrent step execution.

### Constructor

```python
AsyncExecutor(
    executor: Optional[Executor] = None,
    scheduler: Optional[Scheduler] = None,
    max_concurrent: int = 5,
    telemetry: Optional[Telemetry] = None
)
```

**Parameters:**
- `executor`: Synchronous executor
- `scheduler`: DAG scheduler
- `max_concurrent`: Maximum concurrent executions
- `telemetry`: Telemetry instance

### Methods

#### execute_plan

Execute plan asynchronously with concurrency control.

```python
async execute_plan(
    plan: Plan,
    run_id: str,
    resume: bool = True
) -> list[StepResult]
```

**Parameters:**
- `plan`: The execution plan
- `run_id`: Unique run identifier
- `resume`: Whether to resume from previous run

**Returns:** List of step results

**Example:**
```python
import asyncio
from stepchain import AsyncExecutor, Plan

async def main():
    executor = AsyncExecutor(max_concurrent=3)
    results = await executor.execute_plan(plan, "run123")
    
asyncio.run(main())
```

## LLMClient Protocol

Protocol for LLM client implementations.

```python
class LLMClient(Protocol):
    def create_response(
        self,
        input: str,
        tools: list[dict[str, Any]],
        previous_response_id: Optional[str] = None,
        store: bool = True,
        **kwargs: Any,
    ) -> LLMResponse:
        """Create a response from the LLM."""
```

## LLMResponse TypedDict

Type definition for LLM response.

```python
class LLMResponse(TypedDict):
    id: str
    content: str
    tool_calls: NotRequired[list[dict[str, Any]]]
    usage: NotRequired[dict[str, Any]]
```

## Key Features

### Retry Handling
The executor automatically retries failed steps based on the error type:
- Rate limit errors: Exponential backoff
- Server errors: Fixed delay retry
- Tool errors: Immediate retry
- User errors: No retry

### Resume Capability
Executions can be resumed from previous runs by passing `resume=True`. The executor will:
1. Load previous results from storage
2. Skip already completed steps
3. Continue from the last incomplete step

### Dependency Management
The executor ensures steps are executed in the correct order:
- Steps with no dependencies run first
- Steps wait for all dependencies to complete
- Failed dependencies block dependent steps

### Tool Integration
Tools are automatically formatted for the LLM:
```python
tools = ["python_code", "web_search"]
# Converted to OpenAI tool format internally
```

### Error Classification
Errors are automatically classified for appropriate retry strategies:
- `ErrorType.RATE_LIMIT`: API rate limits
- `ErrorType.SERVER_ERROR`: 5xx errors
- `ErrorType.TOOL_ERROR`: Tool execution failures
- `ErrorType.USER_ERROR`: Invalid inputs
- `ErrorType.UNKNOWN`: Unclassified errors