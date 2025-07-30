# Models API Reference

The models module defines the core data structures used throughout the SDK.

## Step

Represents a single step in an execution plan.

### Fields

- `id` (str): Unique identifier for the step
- `prompt` (str): The prompt to send to the LLM
- `tools` (list[str]): List of tools available (default: [])
- `dependencies` (list[str]): Step IDs this depends on (default: [])
- `max_retries` (int): Maximum retry attempts (default: 3)
- `timeout` (Optional[float]): Timeout in seconds (default: None)
- `metadata` (dict[str, Any]): Additional metadata (default: {})

### Validation

- `id`: Must contain only alphanumeric characters, underscores, and hyphens
- `tools`: Tool names must be alphanumeric with underscores/hyphens, max 50 chars
- `prompt`: Cannot be empty

### Example

```python
from stepchain import Step

step = Step(
    id="analyze_data",
    prompt="Analyze the sales data and identify trends",
    tools=["python_code", "data_visualization"],
    dependencies=["fetch_data"],
    max_retries=3,
    timeout=30.0,
    metadata={"priority": "high"}
)
```

## Plan

Execution plan containing multiple steps.

### Fields

- `goal` (str): Goal or objective of the plan (required)
- `id` (str): Plan identifier (default: "default")
- `steps` (list[Step]): List of steps to execute (required)
- `metadata` (dict[str, Any]): Additional metadata (default: {})

### Methods

#### validate_dependencies

Validate that all dependencies reference existing steps.

```python
validate_dependencies() -> None
```

**Raises:** `ValueError` if a dependency references a non-existent step

### Example

```python
from stepchain import Plan, Step

plan = Plan(
    goal="Fetch data from API, process it, and generate a report",
    id="data-pipeline",
    steps=[
        Step(id="fetch", prompt="Fetch data from API"),
        Step(id="process", prompt="Process the data", dependencies=["fetch"]),
        Step(id="report", prompt="Generate report", dependencies=["process"])
    ],
    metadata={"project": "Q4 Analysis"}
)

# Validate the plan
plan.validate_dependencies()
```

## StepResult

Result of executing a single step.

### Fields

- `step_id` (str): ID of the executed step
- `status` (StepStatus): Current status
- `response_id` (Optional[str]): OpenAI response ID
- `previous_response_id` (Optional[str]): Previous response ID for context
- `output` (Optional[dict[str, Any]]): Step output
- `error` (Optional[str]): Error message if failed
- `error_type` (Optional[ErrorType]): Type of error
- `attempt_count` (int): Number of attempts made (default: 1)
- `started_at` (datetime): When execution started
- `completed_at` (Optional[datetime]): When execution completed
- `duration_seconds` (Optional[float]): Execution duration
- `metadata` (dict[str, Any]): Additional metadata

### Methods

#### calculate_duration

Calculate and set duration if completed.

```python
calculate_duration() -> None
```

### Example

```python
from stepchain import StepResult, StepStatus

result = StepResult(
    step_id="analyze",
    status=StepStatus.COMPLETED,
    response_id="resp_123",
    output={"analysis": "Positive trend identified"},
    attempt_count=1
)
result.calculate_duration()
```

## StepStatus

Enum representing the status of a step execution.

### Values

- `PENDING`: Not yet started
- `RUNNING`: Currently executing
- `COMPLETED`: Successfully completed
- `FAILED`: Execution failed
- `RETRYING`: Being retried after failure

### Example

```python
from stepchain import StepStatus

if result.status == StepStatus.COMPLETED:
    print("Step completed successfully")
elif result.status == StepStatus.FAILED:
    print(f"Step failed: {result.error}")
```

## ErrorType

Classification of errors for retry strategies.

### Values

- `RATE_LIMIT`: API rate limit exceeded
- `SERVER_ERROR`: Server-side error (5xx)
- `TOOL_ERROR`: Tool execution failure
- `USER_ERROR`: Invalid user input
- `UNKNOWN`: Unclassified error

### Example

```python
from stepchain import ErrorType

if result.error_type == ErrorType.RATE_LIMIT:
    # Wait before retrying
    time.sleep(60)
elif result.error_type == ErrorType.USER_ERROR:
    # Don't retry, fix the input
    pass
```

## Type Safety

All models use Pydantic for validation and serialization:

```python
# Serialize to JSON
json_data = step.model_dump_json()

# Load from JSON
step = Step.model_validate_json(json_data)

# Convert to dict
dict_data = step.model_dump()

# Validate data
try:
    step = Step(**user_data)
except ValidationError as e:
    print(f"Invalid data: {e}")
```