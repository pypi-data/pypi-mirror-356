"""Unit tests for StepChain models."""

import json
from typing import Any

import pytest
from pydantic import ValidationError

from stepchain.core.models import (
    Plan,
    Step,
    StepResult,
    StepStatus,
    ExecutionState,
    StepExecutionState,
)


class TestStep:
    """Test cases for Step model."""

    def test_step_creation_minimal(self):
        """Test creating a step with minimal required fields."""
        step = Step(
            id="test-step",
            prompt="Test the application",
        )
        assert step.id == "test-step"
        assert step.prompt == "Test the application"
        assert step.dependencies == []
        assert step.tools == []
        assert step.description is None
        assert step.output_schema is None

    def test_step_creation_full(self):
        """Test creating a step with all fields."""
        step = Step(
            id="test-step",
            prompt="Test the application",
            description="Run comprehensive tests",
            dependencies=["setup", "build"],
            tools=["web_search", "code_interpreter"],
            output_schema={"type": "object", "properties": {"result": {"type": "string"}}},
        )
        assert step.id == "test-step"
        assert step.prompt == "Test the application"
        assert step.description == "Run comprehensive tests"
        assert step.dependencies == ["setup", "build"]
        assert step.tools == ["web_search", "code_interpreter"]
        assert step.output_schema == {"type": "object", "properties": {"result": {"type": "string"}}}

    def test_step_id_validation(self):
        """Test step ID validation."""
        # Valid IDs
        valid_ids = ["step1", "step-1", "step_1", "STEP", "123step"]
        for step_id in valid_ids:
            step = Step(id=step_id, prompt="Test")
            assert step.id == step_id

        # Invalid IDs
        invalid_ids = ["step 1", "step.1", "step@1", ""]
        for step_id in invalid_ids:
            with pytest.raises(ValidationError):
                Step(id=step_id, prompt="Test")

    def test_step_serialization(self):
        """Test step serialization to dict and JSON."""
        step = Step(
            id="test-step",
            prompt="Test prompt",
            dependencies=["dep1"],
            tools=["tool1"],
        )
        
        # Test dict serialization
        step_dict = step.model_dump()
        assert step_dict["id"] == "test-step"
        assert step_dict["prompt"] == "Test prompt"
        assert step_dict["dependencies"] == ["dep1"]
        assert step_dict["tools"] == ["tool1"]
        
        # Test JSON serialization
        step_json = step.model_dump_json()
        assert json.loads(step_json) == step_dict

    def test_step_deserialization(self):
        """Test step deserialization from dict."""
        step_data = {
            "id": "test-step",
            "prompt": "Test prompt",
            "dependencies": ["dep1"],
            "tools": ["tool1"],
        }
        step = Step(**step_data)
        assert step.id == "test-step"
        assert step.prompt == "Test prompt"
        assert step.dependencies == ["dep1"]
        assert step.tools == ["tool1"]


class TestPlan:
    """Test cases for Plan model."""

    def test_plan_creation(self):
        """Test creating a plan."""
        steps = [
            Step(id="step1", prompt="First step"),
            Step(id="step2", prompt="Second step", dependencies=["step1"]),
        ]
        plan = Plan(goal="Test goal", steps=steps)
        
        assert plan.goal == "Test goal"
        assert len(plan.steps) == 2
        assert plan.steps[0].id == "step1"
        assert plan.steps[1].dependencies == ["step1"]

    def test_plan_validation_duplicate_step_ids(self):
        """Test that duplicate step IDs are rejected."""
        steps = [
            Step(id="step1", prompt="First step"),
            Step(id="step1", prompt="Duplicate ID"),
        ]
        with pytest.raises(ValidationError, match="Duplicate step IDs found"):
            Plan(goal="Test goal", steps=steps)

    def test_plan_validation_missing_dependency(self):
        """Test that missing dependencies are rejected."""
        steps = [
            Step(id="step1", prompt="First step", dependencies=["missing_step"]),
        ]
        with pytest.raises(ValidationError, match="Step 'step1' depends on non-existent step"):
            Plan(goal="Test goal", steps=steps)

    def test_plan_validation_circular_dependency(self):
        """Test that circular dependencies are rejected."""
        steps = [
            Step(id="step1", prompt="First step", dependencies=["step2"]),
            Step(id="step2", prompt="Second step", dependencies=["step1"]),
        ]
        with pytest.raises(ValidationError, match="Circular dependency detected"):
            Plan(goal="Test goal", steps=steps)

    def test_plan_get_execution_order(self, sample_plan):
        """Test getting execution order respects dependencies."""
        order = sample_plan.get_execution_order()
        
        # step1 should come first (no dependencies)
        assert order[0] == "step1"
        
        # step2 and step3 both depend on step1, so they should come after
        assert set(order[1:]) == {"step2", "step3"}

    def test_plan_get_step_dependencies(self, sample_plan):
        """Test getting step dependencies."""
        deps_map = sample_plan.get_step_dependencies()
        
        assert deps_map["step1"] == []
        assert deps_map["step2"] == ["step1"]
        assert deps_map["step3"] == ["step1"]

    def test_plan_serialization(self):
        """Test plan serialization."""
        steps = [
            Step(id="step1", prompt="First step"),
            Step(id="step2", prompt="Second step"),
        ]
        plan = Plan(goal="Test goal", steps=steps)
        
        # Test dict serialization
        plan_dict = plan.model_dump()
        assert plan_dict["goal"] == "Test goal"
        assert len(plan_dict["steps"]) == 2
        
        # Test JSON serialization
        plan_json = plan.model_dump_json()
        assert json.loads(plan_json) == plan_dict


class TestStepResult:
    """Test cases for StepResult model."""

    def test_step_result_creation_success(self):
        """Test creating a successful step result."""
        result = StepResult(
            step_id="test-step",
            status=StepStatus.COMPLETED,
            content="Success",
            attempt_count=1,
        )
        
        assert result.step_id == "test-step"
        assert result.status == StepStatus.COMPLETED
        assert result.content == "Success"
        assert result.error is None
        assert result.attempt_count == 1

    def test_step_result_creation_failure(self):
        """Test creating a failed step result."""
        result = StepResult(
            step_id="test-step",
            status=StepStatus.FAILED,
            error="Connection timeout",
            attempt_count=3,
        )
        
        assert result.step_id == "test-step"
        assert result.status == StepStatus.FAILED
        assert result.content is None
        assert result.error == "Connection timeout"
        assert result.attempt_count == 3

    def test_step_result_with_output_schema(self):
        """Test step result with structured output."""
        output_data = {"result": "test", "confidence": 0.95}
        result = StepResult(
            step_id="test-step",
            status=StepStatus.COMPLETED,
            content="Success",
            output=output_data,
            attempt_count=1,
        )
        
        assert result.output == output_data

    def test_step_result_serialization(self):
        """Test step result serialization."""
        result = StepResult(
            step_id="test-step",
            status=StepStatus.COMPLETED,
            content="Success",
            attempt_count=1,
        )
        
        # Test dict serialization
        result_dict = result.model_dump()
        assert result_dict["step_id"] == "test-step"
        assert result_dict["status"] == "completed"
        assert result_dict["content"] == "Success"
        
        # Test JSON serialization
        result_json = result.model_dump_json()
        parsed = json.loads(result_json)
        assert parsed["status"] == "completed"  # Enum serialized as string


class TestExecutionState:
    """Test cases for ExecutionState model."""

    def test_execution_state_creation(self):
        """Test creating an execution state."""
        state = ExecutionState(
            run_id="test-run",
            plan=Plan(goal="Test", steps=[Step(id="s1", prompt="Test")]),
            status="running",
        )
        
        assert state.run_id == "test-run"
        assert state.plan.goal == "Test"
        assert state.status == "running"
        assert state.completed_steps == []
        assert state.step_states == {}

    def test_execution_state_with_step_states(self, sample_plan):
        """Test execution state with step states."""
        step_states = {
            "step1": StepExecutionState(
                step_id="step1",
                status=StepStatus.COMPLETED,
                result=StepResult(
                    step_id="step1",
                    status=StepStatus.COMPLETED,
                    content="Done",
                    attempt_count=1,
                ),
            )
        }
        
        state = ExecutionState(
            run_id="test-run",
            plan=sample_plan,
            status="running",
            completed_steps=["step1"],
            step_states=step_states,
        )
        
        assert state.completed_steps == ["step1"]
        assert "step1" in state.step_states
        assert state.step_states["step1"].status == StepStatus.COMPLETED

    def test_execution_state_serialization(self, sample_plan):
        """Test execution state serialization."""
        state = ExecutionState(
            run_id="test-run",
            plan=sample_plan,
            status="running",
            completed_steps=["step1"],
        )
        
        # Test dict serialization
        state_dict = state.model_dump()
        assert state_dict["run_id"] == "test-run"
        assert state_dict["status"] == "running"
        assert state_dict["completed_steps"] == ["step1"]
        
        # Test JSON serialization
        state_json = state.model_dump_json()
        parsed = json.loads(state_json)
        assert parsed["run_id"] == "test-run"


class TestStepStatus:
    """Test cases for StepStatus enum."""

    def test_step_status_values(self):
        """Test StepStatus enum values."""
        assert StepStatus.PENDING.value == "pending"
        assert StepStatus.RUNNING.value == "running"
        assert StepStatus.COMPLETED.value == "completed"
        assert StepStatus.FAILED.value == "failed"
        assert StepStatus.SKIPPED.value == "skipped"

    def test_step_status_comparison(self):
        """Test StepStatus enum comparison."""
        assert StepStatus.PENDING != StepStatus.RUNNING
        assert StepStatus.COMPLETED == StepStatus.COMPLETED
        
    def test_step_status_serialization(self):
        """Test StepStatus enum serialization."""
        status = StepStatus.COMPLETED
        assert status.value == "completed"
        assert json.dumps(status.value) == '"completed"'