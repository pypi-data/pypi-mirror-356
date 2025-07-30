# Decomposer API Reference

The decomposer module provides intelligent task decomposition using LLMs.

## TaskDecomposer

The main class for decomposing complex tasks into executable steps.

### Constructor

```python
TaskDecomposer(
    llm_client: Optional[LLMClient] = None,
    strategy: DecompositionStrategy = DecompositionStrategy.HYBRID,
    max_steps: int = 20,
    validate_plans: bool = True,
    model: str = "gpt-4o-mini"
)
```

**Parameters:**
- `llm_client`: LLM client for generating decompositions (defaults to OpenAI)
- `strategy`: Decomposition strategy to use
- `max_steps`: Maximum allowed steps in a plan (must be >= 1)
- `validate_plans`: Whether to validate generated plans
- `model`: LLM model to use for decomposition

### Methods

#### decompose

Decompose a complex task into a plan with steps.

```python
decompose(
    task_description: str,
    available_tools: Optional[List[str]] = None,
    context: Optional[Dict[str, Any]] = None,
    retry_on_validation_failure: bool = True
) -> Plan
```

**Parameters:**
- `task_description`: Natural language description of the task
- `available_tools`: List of available tool names (defaults to standard tools)
- `context`: Additional context for decomposition
- `retry_on_validation_failure`: Whether to retry if validation fails

**Returns:** `Plan` object with decomposed steps

**Raises:**
- `DecompositionError`: If decomposition fails
- `PlanValidationError`: If plan validation fails
- `LLMError`: If LLM interaction fails

**Example:**
```python
decomposer = TaskDecomposer(strategy=DecompositionStrategy.HIERARCHICAL)
plan = decomposer.decompose(
    "Create a data analysis report comparing sales trends across regions",
    available_tools=["python_code", "data_visualization"]
)
```

## DecompositionStrategy

Enum defining available decomposition strategies:

- `HIERARCHICAL`: Top-down breakdown into subtasks
- `SEQUENTIAL`: Linear step-by-step approach
- `PARALLEL`: Maximize parallelization
- `HYBRID`: Mix of sequential and parallel

## TemplateBasedDecomposer

Decomposes tasks using predefined templates for common patterns.

### Constructor

```python
TemplateBasedDecomposer()
```

Initializes with default templates for data analysis and web research.

### Methods

#### register_template

Register a new template.

```python
register_template(
    name: str,
    matcher: callable,
    template: Dict[str, Any]
) -> None
```

**Parameters:**
- `name`: Template name
- `matcher`: Function to check if template applies
- `template`: Template structure

#### decompose

Decompose using templates.

```python
decompose(
    task_description: str,
    available_tools: Optional[List[str]] = None,
    **kwargs
) -> Plan
```

**Parameters:**
- `task_description`: Task to decompose
- `available_tools`: Available tools

**Returns:** Generated plan

**Raises:** `DecompositionError` if no matching template found

## DecomposerFactory

Factory for creating task decomposers.

### Methods

#### register

Register a decomposer class.

```python
register(name: str, decomposer_class: Type[BaseDecomposer]) -> None
```

#### create

Create a decomposer instance.

```python
create(name: str, **kwargs) -> BaseDecomposer
```

**Parameters:**
- `name`: Name of decomposer to create
- `**kwargs`: Arguments for decomposer constructor

**Returns:** Decomposer instance

**Raises:** `ValueError` if decomposer name not found

#### list_available

List available decomposer names.

```python
list_available() -> List[str]
```

**Returns:** List of registered names

## Exceptions

- `DecompositionError`: Base exception for decomposition errors
- `PlanValidationError`: Raised when plan validation fails
- `LLMError`: Raised when LLM interaction fails

## Default Tools

When no tools are specified, the following defaults are available:
- `web_search`
- `database_query`
- `python_code`
- `file_operations`
- `data_visualization`
- `statistical_analysis`
- `api_calls`
- `text_processing`
- `image_generation`
- `email`
- `calendar`