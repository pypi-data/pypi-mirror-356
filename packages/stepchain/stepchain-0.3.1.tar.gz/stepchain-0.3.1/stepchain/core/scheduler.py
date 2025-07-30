"""Task scheduling and dependency management.

This module provides DAG-based scheduling for step execution.
"""

import asyncio
import logging
from collections import defaultdict

from stepchain.config import get_config
from stepchain.core.executor import Executor
from stepchain.core.models import ErrorType, Plan, Step, StepResult, StepStatus
from stepchain.utils.telemetry import Telemetry

logger = logging.getLogger(__name__)


class Scheduler:
    """Simple DAG scheduler for step execution.

    Example:
        >>> plan = Plan(steps=[
        ...     Step(id="a", prompt="First"),
        ...     Step(id="b", prompt="Second", dependencies=["a"]),
        ... ])
        >>> scheduler = Scheduler()
        >>> order = scheduler.get_execution_order(plan)
        >>> assert order == ["a", "b"]
    """

    def get_execution_order(self, plan: Plan) -> list[str]:
        """Get topologically sorted execution order.

        Args:
            plan: The execution plan

        Returns:
            List of step IDs in execution order

        Raises:
            ValueError: If circular dependencies exist
        """
        # Build adjacency list
        graph = defaultdict(list)
        in_degree = defaultdict(int)
        all_steps = {step.id for step in plan.steps}

        for step in plan.steps:
            for dep in step.dependencies:
                graph[dep].append(step.id)
                in_degree[step.id] += 1

        # Kahn's algorithm
        queue = [step_id for step_id in all_steps if in_degree[step_id] == 0]
        result = []

        while queue:
            current = queue.pop(0)
            result.append(current)

            for neighbor in graph[current]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        if len(result) != len(all_steps):
            raise ValueError("Circular dependencies detected in plan")

        return result

    def get_ready_steps(
        self,
        plan: Plan,
        completed: set[str],
        running: set[str],
    ) -> list[Step]:
        """Get steps that are ready to execute.

        Args:
            plan: The execution plan
            completed: Set of completed step IDs
            running: Set of currently running step IDs

        Returns:
            List of steps ready to execute
        """
        ready = []
        for step in plan.steps:
            if step.id in completed or step.id in running:
                continue
            if all(dep in completed for dep in step.dependencies):
                ready.append(step)
        return ready


class AsyncExecutor:
    """Asynchronous executor with concurrent step execution.

    Example:
        >>> import asyncio
        >>> async def main():
        ...     executor = AsyncExecutor(max_concurrent=3)
        ...     results = await executor.execute_plan(plan, "run123")
    """

    def __init__(
        self,
        executor: Executor | None = None,
        scheduler: Scheduler | None = None,
        max_concurrent: int | None = None,
        telemetry: Telemetry | None = None,
    ):
        """Initialize async executor.

        Args:
            executor: Synchronous executor
            scheduler: DAG scheduler
            max_concurrent: Maximum concurrent executions
            telemetry: Telemetry instance
        """
        self.config = get_config()
        self.executor = executor or Executor()
        self.scheduler = scheduler or Scheduler()
        self.max_concurrent = max_concurrent or self.config.max_concurrent_steps
        self.semaphore = asyncio.Semaphore(self.max_concurrent)
        self.telemetry = (
            telemetry if telemetry is not None
            else (Telemetry() if self.config.enable_telemetry else None)
        )

    async def execute_plan(
        self,
        plan: Plan,
        run_id: str,
        resume: bool = True,
    ) -> list[StepResult]:
        """Execute plan asynchronously with concurrency control.

        Args:
            plan: The execution plan
            run_id: Unique run identifier
            resume: Whether to resume from previous run

        Returns:
            List of step results
        """
        if self.telemetry:
            async with self.telemetry.async_span("async_execute_plan", {"run_id": run_id}):
                return await self._execute_plan_impl(plan, run_id, resume)
        else:
            return await self._execute_plan_impl(plan, run_id, resume)
    
    async def _execute_plan_impl(
        self,
        plan: Plan,
        run_id: str,
        resume: bool,
    ) -> list[StepResult]:
        """Implementation of plan execution."""
        plan.validate_dependencies()

        # Get previous results
        previous_results = []
        completed = set()
        if resume:
            previous_results = self.executor.store.get_results(run_id)
            completed = {r.step_id for r in previous_results if r.status == StepStatus.COMPLETED}

        running = set()
        results = []

        # Create tasks for ready steps
        tasks = {}
        
        while len(completed) < len(plan.steps):
            # Get ready steps
            ready = self.scheduler.get_ready_steps(plan, completed, running)
            
            # Start tasks for ready steps
            for step in ready:
                if step.id not in tasks:
                    task = asyncio.create_task(
                        self._execute_step_async(step, run_id, previous_results)
                    )
                    tasks[step.id] = task
                    running.add(step.id)
            
            if not tasks:
                # No tasks running and none ready - might be a failure
                break
            
            # Wait for at least one task to complete with a global timeout
            try:
                done, pending = await asyncio.wait(
                    tasks.values(),
                    return_when=asyncio.FIRST_COMPLETED,
                    timeout=300  # 5 minute global timeout for any single wait
                )
            except TimeoutError:
                logger.warning("Global wait timeout reached, checking task status")
                done = set()
            
            # Process completed tasks
            for task in done:
                try:
                    result = await task
                    results.append(result)
                    
                    # Find which step this was
                    for step_id, t in list(tasks.items()):
                        if t == task:
                            del tasks[step_id]
                            running.remove(step_id)
                            
                            if result.status == StepStatus.COMPLETED:
                                completed.add(step_id)
                                previous_results.append(result)
                            elif result.status == StepStatus.FAILED:
                                logger.error(f"Step {step_id} failed: {result.error}")
                                # Mark dependent steps as blocked
                                for step in plan.steps:
                                    if step_id in step.dependencies and step.id not in completed:
                                        logger.warning(
                                            f"Step {step.id} blocked due to "
                                            f"failure of {step_id}"
                                        )
                            break
                except Exception as e:
                    logger.error(f"Task execution error: {e}")
                    # Find and remove the failed task
                    for step_id, t in list(tasks.items()):
                        if t == task:
                            del tasks[step_id]
                            running.remove(step_id)
                            break
        
        return results

    async def _execute_step_async(
        self,
        step: Step,
        run_id: str,
        previous_results: list[StepResult],
    ) -> StepResult:
        """Execute a step asynchronously with semaphore control and timeout."""
        async with self.semaphore:
            try:
                # Run the synchronous executor in a thread pool with timeout
                loop = asyncio.get_event_loop()
                
                # Create the execution task
                execution_task = loop.run_in_executor(
                    None,
                    self.executor._execute_step,
                    step,
                    run_id,
                    previous_results,
                )
                
                # Apply timeout if specified
                timeout = step.timeout or self.config.openai_timeout
                
                try:
                    result = await asyncio.wait_for(execution_task, timeout=timeout)
                except TimeoutError:
                    logger.error(f"Step {step.id} timed out after {timeout}s")
                    # Create a timeout result
                    result = StepResult(
                        step_id=step.id,
                        status=StepStatus.FAILED,
                        error=f"Step execution timed out after {timeout} seconds",
                        error_type=ErrorType.UNKNOWN,
                        attempt_count=1,
                    )
                    result.calculate_duration()
                    
                self.executor.store.save_result(run_id, result)
                return result
                
            except Exception as e:
                logger.error(f"Failed to execute step {step.id}: {e}", exc_info=True)
                # Create a failed result
                result = StepResult(
                    step_id=step.id,
                    status=StepStatus.FAILED,
                    error=str(e),
                    error_type=ErrorType.UNKNOWN,
                    attempt_count=1,
                )
                result.calculate_duration()
                self.executor.store.save_result(run_id, result)
                return result
