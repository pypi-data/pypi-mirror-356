"""Storage backends for persisting step results.

This module provides abstractions for storing and retrieving execution results.
"""

import json
import logging
from abc import ABC, abstractmethod
from collections.abc import Iterator
from pathlib import Path
from typing import TYPE_CHECKING, Optional

from stepchain.core.models import StepResult

if TYPE_CHECKING:
    from stepchain.core.models import Plan

logger = logging.getLogger(__name__)


class AbstractStore(ABC):
    """Abstract base class for storage backends.

    Example:
        >>> class MemoryStore(AbstractStore):
        ...     def __init__(self) -> None:
        ...         self.results = {}
        ...     def save_result(self, run_id: str, result: StepResult) -> None:
        ...         self.results.setdefault(run_id, []).append(result)
    """

    @abstractmethod
    def save_result(self, run_id: str, result: StepResult) -> None:
        """Save a step result."""
        pass

    @abstractmethod
    def get_results(self, run_id: str) -> list[StepResult]:
        """Get all results for a run."""
        pass

    @abstractmethod
    def get_latest_result(self, run_id: str, step_id: str) -> StepResult | None:
        """Get the latest result for a specific step."""
        pass

    @abstractmethod
    def list_runs(self) -> list[str]:
        """List all run IDs."""
        pass
    
    @abstractmethod 
    def save_plan(self, run_id: str, plan: 'Plan') -> None:
        """Save the execution plan for a run."""
        pass
    
    @abstractmethod
    def get_plan(self, run_id: str) -> Optional['Plan']:
        """Get the execution plan for a run."""
        pass


class JSONLStore(AbstractStore):
    """JSON Lines file-based storage.

    Example:
        >>> store = JSONLStore(base_path="/tmp/taskcrew")
        >>> result = StepResult(step_id="test", status=StepStatus.COMPLETED)
        >>> store.save_result("run123", result)
        >>> results = store.get_results("run123")
    """

    def __init__(self, base_path: str = ".stepchain"):
        """Initialize JSONL store.

        Args:
            base_path: Directory to store JSONL files
        """
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Initialized JSONLStore at {self.base_path}")

    def _get_run_file(self, run_id: str) -> Path:
        """Get the file path for a run."""
        return self.base_path / f"{run_id}.jsonl"

    def save_result(self, run_id: str, result: StepResult) -> None:
        """Save a step result to JSONL file."""
        file_path = self._get_run_file(run_id)
        with open(file_path, "a") as f:
            # Manually extract data to avoid Pydantic serialization issues
            data = {
                "step_id": result.step_id,
                "status": (
                    result.status.value if hasattr(result.status, 'value')
                    else str(result.status)
                ),
                "attempt_count": result.attempt_count,
            }
            
            # Add optional fields if present
            if result.content is not None:
                data["content"] = result.content
            if result.response_id is not None:
                data["response_id"] = result.response_id
            if result.previous_response_id is not None:
                data["previous_response_id"] = result.previous_response_id
            if result.output is not None:
                # Ensure output is JSON serializable
                if isinstance(result.output, dict):
                    data["output"] = result.output
                else:
                    data["output"] = str(result.output)
            if result.error is not None:
                data["error"] = result.error
            if result.error_type is not None:
                data["error_type"] = (
                    result.error_type.value if hasattr(result.error_type, 'value')
                    else str(result.error_type)
                )
            if result.duration_seconds is not None:
                data["duration_seconds"] = result.duration_seconds
            if result.metadata:
                # Remove sensitive metadata
                data["metadata"] = {k: v for k, v in result.metadata.items() if k != "auth_token"}
            
            # Handle datetime fields
            if hasattr(result.started_at, "isoformat"):
                data["started_at"] = result.started_at.isoformat()
            else:
                data["started_at"] = str(result.started_at)
                
            if result.completed_at:
                if hasattr(result.completed_at, "isoformat"):
                    data["completed_at"] = result.completed_at.isoformat()
                else:
                    data["completed_at"] = str(result.completed_at)
                    
            f.write(json.dumps(data) + "\n")
        logger.debug(f"Saved result for step {result.step_id} to {file_path}")

    def get_results(self, run_id: str) -> list[StepResult]:
        """Get all results for a run.
        
        For better performance with large files, consider using iter_results().
        """
        return list(self.iter_results(run_id))

    def get_latest_result(self, run_id: str, step_id: str) -> StepResult | None:
        """Get the latest result for a specific step."""
        results = self.get_results(run_id)
        step_results = [r for r in results if r.step_id == step_id]
        return step_results[-1] if step_results else None

    def list_runs(self) -> list[str]:
        """List all run IDs."""
        return [f.stem for f in self.base_path.glob("*.jsonl")]

    def iter_results(self, run_id: str) -> Iterator[StepResult]:
        """Iterate over results without loading all into memory.
        
        This is more memory-efficient for large result sets.
        """
        file_path = self._get_run_file(run_id)
        if not file_path.exists():
            return

        with open(file_path, buffering=8192) as f:  # Use buffered reading
            for line_num, line in enumerate(f, 1):
                if line.strip():
                    try:
                        data = json.loads(line)
                        yield StepResult(**data)
                    except json.JSONDecodeError as e:
                        logger.warning(
                            f"Skipping malformed JSON at line {line_num} "
                            f"in {file_path}: {e}"
                        )
                        continue
                    except Exception as e:
                        logger.warning(
                            f"Error parsing result at line {line_num} "
                            f"in {file_path}: {e}"
                        )
                        continue
    
    def save_plan(self, run_id: str, plan: 'Plan') -> None:
        """Save the execution plan for a run."""
        plan_file = self.base_path / f"{run_id}_plan.json"
        with open(plan_file, "w") as f:
            # Manually build plan dict to avoid serialization issues
            plan_dict = {
                "id": plan.id,
                "steps": []
            }
            
            if plan.metadata:
                plan_dict["metadata"] = plan.metadata  # type: ignore
                
            # Convert each step
            for step in plan.steps:
                step_dict = {
                    "id": step.id,
                    "prompt": step.prompt,
                    "tools": step.tools,
                    "dependencies": step.dependencies,
                    "max_retries": step.max_retries,
                }
                if step.timeout is not None:
                    step_dict["timeout"] = step.timeout
                if step.metadata:
                    step_dict["metadata"] = step.metadata
                plan_dict["steps"].append(step_dict)
                
            json.dump(plan_dict, f, indent=2)
        logger.debug(f"Saved plan for run {run_id} to {plan_file}")
    
    def get_plan(self, run_id: str) -> Optional['Plan']:
        """Get the execution plan for a run."""
        from stepchain.core.models import Plan
        
        plan_file = self.base_path / f"{run_id}_plan.json"
        if not plan_file.exists():
            return None
            
        with open(plan_file) as f:
            plan_data = json.load(f)
            # Add required goal field if missing
            if "goal" not in plan_data:
                original_task = plan_data.get("metadata", {}).get("original_task", "Unknown task")
                plan_data["goal"] = original_task
            return Plan(**plan_data)


class MemoryStore(AbstractStore):
    """In-memory storage for testing and development.
    
    Example:
        >>> store = MemoryStore()
        >>> result = StepResult(step_id="test", status=StepStatus.COMPLETED)
        >>> store.save_result("run123", result)
        >>> assert len(store.get_results("run123")) == 1
    """
    
    def __init__(self) -> None:
        """Initialize memory store."""
        self.results: dict[str, list[StepResult]] = {}
        self.plans: dict[str, Plan] = {}
        logger.info("Initialized MemoryStore")
    
    def save_result(self, run_id: str, result: StepResult) -> None:
        """Save a step result in memory."""
        if run_id not in self.results:
            self.results[run_id] = []
        self.results[run_id].append(result)
        logger.debug(f"Saved result for step {result.step_id} in memory")
    
    def get_results(self, run_id: str) -> list[StepResult]:
        """Get all results for a run."""
        return self.results.get(run_id, [])
    
    def get_latest_result(self, run_id: str, step_id: str) -> StepResult | None:
        """Get the latest result for a specific step."""
        results = self.get_results(run_id)
        step_results = [r for r in results if r.step_id == step_id]
        return step_results[-1] if step_results else None
    
    def list_runs(self) -> list[str]:
        """List all run IDs."""
        return list(self.results.keys())
    
    def save_plan(self, run_id: str, plan: 'Plan') -> None:
        """Save the execution plan for a run."""
        self.plans[run_id] = plan
        logger.debug(f"Saved plan for run {run_id} in memory")
    
    def get_plan(self, run_id: str) -> Optional['Plan']:
        """Get the execution plan for a run."""
        return self.plans.get(run_id)
