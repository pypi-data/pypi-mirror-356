# StepChain API Reference

## Table of Contents
- [Core Functions](#core-functions)
  - [decompose()](#decompose)
  - [execute()](#execute)
  - [setup_stepchain()](#setup_stepchain)
- [Classes](#classes)
  - [Executor](#executor)
  - [TaskDecomposer](#taskdecomposer)
  - [Plan](#plan)
  - [Step](#step)
  - [StepResult](#stepresult)
- [Tool Definitions](#tool-definitions)
  - [MCP Tools](#mcp-tools)
  - [Function Tools](#function-tools)
  - [Built-in Tools](#built-in-tools)
- [Error Handling](#error-handling)
- [Storage Format](#storage-format)

## Core Functions

### decompose()

Decomposes a complex task into executable steps using OpenAI's Responses API.

```python
def decompose(
    task: str,
    tools: list[Union[str, dict]] = None,
    model: str = "gpt-4",
    max_steps: int = 50,
    temperature: float = 0.2
) -> Plan
```

#### Parameters

- **task** (str): The task description to decompose
- **tools** (list, optional): Available tools for the task. Can include:
  - String identifiers for built-in tools: `"web_search"`, `"code_interpreter"`, `"file_search"`
  - MCP tool definitions (dict)
  - Function tool definitions (dict)
- **model** (str): OpenAI model to use. Default: `"gpt-4"`
- **max_steps** (int): Maximum number of steps to generate. Default: `50`
- **temperature** (float): Model temperature for generation. Default: `0.2`

#### Returns

- **Plan**: A plan object containing the decomposed steps

#### Example

```python
# Simple decomposition
plan = decompose("Analyze sales data and create a report")

# With tools
plan = decompose(
    "Search for Python news and summarize",
    tools=["web_search", {"type": "mcp", "server_label": "news_api", ...}]
)
```

### execute()

Executes a plan with automatic retry and state persistence.

```python
def execute(
    plan: Plan,
    run_id: str = None,
    resume: bool = False,
    max_concurrent: int = 3
) -> list[StepResult]
```

#### Parameters

- **plan** (Plan): The plan to execute (from `decompose()`)
- **run_id** (str, optional): Unique identifier for this execution. Required for resume capability
- **resume** (bool): Whether to resume from a previous execution. Default: `False`
- **max_concurrent** (int): Maximum concurrent step executions. Default: `3`

#### Returns

- **list[StepResult]**: Results for each executed step

#### Example

```python
# Execute a plan
results = execute(plan)

# Execute with resume capability
results = execute(plan, run_id="analysis_001")

# Resume after failure
results = execute(plan, run_id="analysis_001", resume=True)
```

### setup_stepchain()

Initializes StepChain with default configuration.

```python
def setup_stepchain(
    storage_path: str = ".stepchain",
    log_level: str = "INFO"
) -> Config
```

#### Parameters

- **storage_path** (str): Directory for state storage. Default: `".stepchain"`
- **log_level** (str): Logging level. Default: `"INFO"`

#### Returns

- **Config**: Configuration object with initialized settings

## Classes

### Executor

Main execution engine for plans.

```python
class Executor:
    def __init__(
        self,
        max_concurrent: int = 3,
        timeout: int = 300,
        retry_attempts: int = 1,
        function_registry: FunctionRegistry = None
    )
```

#### Methods

##### execute_plan()

```python
def execute_plan(
    self,
    plan: Plan,
    run_id: str = None,
    resume: bool = False
) -> list[StepResult]
```

Executes a plan with full state management.

##### execute_step()

```python
async def execute_step(
    self,
    step: Step,
    context: dict = None
) -> StepResult
```

Executes a single step (used internally).

#### Example

```python
# Custom executor with configuration
executor = Executor(
    max_concurrent=5,
    timeout=600,  # 10 minutes per step
    retry_attempts=2
)

results = executor.execute_plan(plan, run_id="custom_run")
```

### TaskDecomposer

Handles task decomposition using OpenAI's API.

```python
class TaskDecomposer:
    def __init__(
        self,
        client: UnifiedLLMClient = None,
        model: str = "gpt-4",
        max_steps: int = 50
    )
```

#### Methods

##### decompose()

```python
def decompose(
    self,
    task_description: str,
    tools: list[dict] = None,
    temperature: float = 0.2
) -> Plan
```

### Plan

Represents a decomposed task plan.

```python
@dataclass
class Plan:
    task_description: str
    steps: list[Step]
    metadata: dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
```

#### Attributes

- **task_description** (str): Original task description
- **steps** (list[Step]): Ordered list of steps
- **metadata** (dict): Additional plan metadata
- **created_at** (datetime): Plan creation timestamp

### Step

Represents a single executable step.

```python
@dataclass
class Step:
    id: str
    description: str
    tool: str = None
    tool_input: dict = None
    dependencies: list[str] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
```

#### Attributes

- **id** (str): Unique step identifier (e.g., "step_1")
- **description** (str): Human-readable step description
- **tool** (str, optional): Tool to use for this step
- **tool_input** (dict, optional): Input parameters for the tool
- **dependencies** (list[str]): IDs of steps that must complete first
- **metadata** (dict): Additional step metadata

### StepResult

Result of executing a step.

```python
@dataclass
class StepResult:
    step_id: str
    status: Literal["completed", "failed", "skipped"]
    output: Any = None
    error: str = None
    started_at: datetime = None
    completed_at: datetime = None
    attempts: int = 0
```

#### Attributes

- **step_id** (str): ID of the executed step
- **status** (str): Execution status
- **output** (Any): Step output (tool-specific)
- **error** (str, optional): Error message if failed
- **started_at** (datetime): Execution start time
- **completed_at** (datetime): Execution end time
- **attempts** (int): Number of execution attempts

## Tool Definitions

### MCP Tools

Model Context Protocol server integration.

```python
mcp_tool = {
    "type": "mcp",
    "server_label": "github",  # Unique identifier
    "server_url": "https://github.mcp.com/org/repo",  # Server endpoint
    "allowed_tools": ["search_code", "read_file"],    # Available tools
    "require_approval": "never",  # "never" or "always"
    
    # Optional fields
    "server_command": "python",  # Command to start server
    "server_args": ["-m", "mcp_server_github"],  # Arguments
    "timeout": 30,  # Request timeout in seconds
    "env": {  # Environment variables
        "API_KEY": "..."
    }
}
```

### Function Tools

Custom Python function integration.

```python
def my_function(param1: str, param2: int = 10) -> dict:
    """Function implementation."""
    return {"result": param1 * param2}

function_tool = {
    "type": "function",
    "function": {
        "name": "my_function",
        "description": "Repeats a string multiple times",
        "parameters": {
            "type": "object",
            "properties": {
                "param1": {
                    "type": "string",
                    "description": "String to repeat"
                },
                "param2": {
                    "type": "integer",
                    "description": "Number of repetitions",
                    "default": 10
                }
            },
            "required": ["param1"]
        }
    },
    "implementation": my_function  # Reference to the function
}
```

### Built-in Tools

StepChain provides these built-in tools:

- **web_search**: Search the web for information
- **code_interpreter**: Execute Python code in a sandbox
- **file_search**: Search through uploaded files (requires `vector_store_ids`)

```python
# Using built-in tools
plan = decompose(
    "Research and analyze data",
    tools=["web_search", "code_interpreter"]
)
```

## Error Handling

StepChain uses typed errors for different failure scenarios:

```python
from stepchain.core.types import ErrorType

# Error types
ErrorType.RATE_LIMIT     # API rate limit exceeded
ErrorType.SERVER_ERROR   # API server error
ErrorType.TOOL_ERROR     # Tool execution failed
ErrorType.VALIDATION     # Response validation failed
ErrorType.TIMEOUT        # Step execution timeout
ErrorType.UNKNOWN        # Unexpected error
```

### Handling Errors

```python
results = execute(plan, run_id="task_001")

for result in results:
    if result.status == "failed":
        print(f"Step {result.step_id} failed: {result.error}")
        # Check error type in result.metadata["error_type"]
```

## Storage Format

StepChain persists state in JSONL format:

```jsonl
{"timestamp": "2024-01-15T10:00:00Z", "type": "plan", "run_id": "task_001", "data": {...}}
{"timestamp": "2024-01-15T10:00:01Z", "type": "step_started", "run_id": "task_001", "step_id": "step_1"}
{"timestamp": "2024-01-15T10:00:05Z", "type": "step_completed", "run_id": "task_001", "step_id": "step_1", "output": {...}}
```

### Storage Location

Default: `.stepchain/runs/{run_id}.jsonl`

### Reading Storage

```python
from stepchain.core.storage import Storage

storage = Storage()
state = storage.load_run_state("task_001")

# Access plan and results
plan = state.plan
results = state.results
```

## Advanced Usage

### Custom Retry Logic

```python
from stepchain.core.executor import retry_on_exception

@retry_on_exception(max_attempts=3, backoff_base=2)
def custom_operation():
    # Your code here
    pass
```

### Parallel Execution Control

```python
# Limit concurrent executions
executor = Executor(max_concurrent=1)  # Sequential execution
executor = Executor(max_concurrent=10)  # High parallelism

# Dynamic concurrency based on step type
class CustomExecutor(Executor):
    def get_max_concurrent(self, step: Step) -> int:
        if step.tool == "web_search":
            return 5  # Allow parallel web searches
        return 1  # Sequential for other tools
```

### Custom Storage Backend

```python
from stepchain.core.storage import Storage

class S3Storage(Storage):
    def save_state(self, run_id: str, entry: dict):
        # Custom S3 implementation
        pass
    
    def load_run_state(self, run_id: str):
        # Custom S3 implementation
        pass

# Use custom storage
executor = Executor()
executor.storage = S3Storage()
```

## Environment Variables

- `OPENAI_API_KEY`: Required for OpenAI API access
- `STEPCHAIN_STORAGE_PATH`: Override default storage location
- `STEPCHAIN_LOG_LEVEL`: Set logging level (DEBUG, INFO, WARNING, ERROR)
- `STEPCHAIN_MAX_RETRIES`: Global retry limit override

## Thread Safety

StepChain is thread-safe for:
- Multiple concurrent `decompose()` calls
- Multiple concurrent `execute()` calls with different `run_id`s
- Reading storage while executing

Not thread-safe for:
- Multiple `execute()` calls with the same `run_id`
- Modifying executor configuration during execution