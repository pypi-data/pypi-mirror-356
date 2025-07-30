"""StepChain SDK - AI-powered task decomposition and execution.

StepChain breaks down complex multi-tool tasks into discrete steps with
dependencies, executes them with smart retries and parallelization, and provides
robust state management for resumable workflows.

Example:
    >>> from stepchain import TaskDecomposer, Executor
    >>> 
    >>> # Decompose a complex task
    >>> decomposer = TaskDecomposer()
    >>> plan = decomposer.decompose(
    ...     "Analyze customer feedback data and create a presentation"
    ... )
    >>> 
    >>> # Execute the plan
    >>> executor = Executor()
    >>> results = executor.execute_plan(plan, run_id="analysis_001")
    
    Or manually create a plan:
    
    >>> from stepchain import Plan, Step
    >>> plan = Plan(
    ...     steps=[
    ...         Step(id="fetch", prompt="Fetch data from API"),
    ...         Step(id="analyze", prompt="Analyze the data", dependencies=["fetch"]),
    ...     ]
    ... )
"""

from stepchain.config import Config, get_config, setup_stepchain
from stepchain.core.decomposer import TaskDecomposer
from stepchain.core.executor import Executor
from stepchain.core.models import Plan, Step, StepResult, StepStatus
from stepchain.core.scheduler import AsyncExecutor
from stepchain.function_registry import FunctionRegistry
from stepchain.storage.jsonl import JSONLStore

__version__ = "0.3.1"  # Simplified API with 10x developer approach
__all__ = [
    "AsyncExecutor",
    "Config",
    "Executor",
    "FunctionRegistry",
    "JSONLStore",
    "Plan",
    "Step",
    "StepResult",
    "StepStatus",
    "TaskDecomposer",
    "decompose",
    "execute",
    "get_config",
    "setup_stepchain",
]

# Convenience imports for the simple API
from stepchain.core.decomposer import decompose


def execute(plan: Plan, run_id: str | None = None, resume: bool = False) -> list[StepResult]:
    """Execute a plan with automatic state management.
    
    Args:
        plan: The plan to execute
        run_id: Unique identifier for this run (auto-generated if not provided)
        resume: Whether to resume from a previous run
        
    Returns:
        List of step results
    """
    from stepchain.core.executor import Executor
    if run_id is None:
        import uuid
        run_id = str(uuid.uuid4())[:8]
    
    executor = Executor()
    return executor.execute_plan(plan, run_id=run_id, resume=resume)