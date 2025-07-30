"""Unit tests for storage components."""

import json
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, mock_open, patch

import pytest

from stepchain.core.models import ExecutionState, Plan, Step, StepResult, StepStatus
from stepchain.storage import JSONLStore


class TestJSONLStore:
    """Test cases for JSONLStore."""

    @pytest.fixture
    def store(self, temp_storage_dir):
        """Create a JSONLStore instance for testing."""
        return JSONLStore(storage_path=temp_storage_dir, run_id="test-run")

    @pytest.fixture
    def sample_result(self):
        """Create a sample step result."""
        return StepResult(
            step_id="test-step",
            status=StepStatus.COMPLETED,
            content="Test content",
            attempt_count=1,
        )

    def test_store_initialization(self, temp_storage_dir):
        """Test JSONLStore initialization."""
        store = JSONLStore(storage_path=temp_storage_dir, run_id="test-run")
        
        assert store.storage_path == temp_storage_dir
        assert store.run_id == "test-run"
        assert store.output_file == temp_storage_dir / "test-run.jsonl"

    def test_store_ensure_storage_path(self, tmp_path):
        """Test that storage path is created if it doesn't exist."""
        non_existent_path = tmp_path / "new_dir"
        store = JSONLStore(storage_path=non_existent_path, run_id="test")
        
        assert non_existent_path.exists()
        assert non_existent_path.is_dir()

    def test_save_result(self, store, sample_result):
        """Test saving a step result."""
        store.save_result(sample_result)
        
        # Read the file and verify content
        with open(store.output_file, "r") as f:
            lines = f.readlines()
        
        assert len(lines) == 1
        
        # Parse the saved data
        saved_data = json.loads(lines[0])
        
        assert saved_data["type"] == "step_result"
        assert saved_data["run_id"] == "test-run"
        assert saved_data["data"]["step_id"] == "test-step"
        assert saved_data["data"]["status"] == "completed"
        assert saved_data["data"]["content"] == "Test content"
        assert "timestamp" in saved_data

    def test_save_multiple_results(self, store):
        """Test saving multiple results."""
        results = [
            StepResult(
                step_id=f"step-{i}",
                status=StepStatus.COMPLETED,
                content=f"Content {i}",
                attempt_count=1,
            )
            for i in range(3)
        ]
        
        for result in results:
            store.save_result(result)
        
        # Read and verify all results
        with open(store.output_file, "r") as f:
            lines = f.readlines()
        
        assert len(lines) == 3
        
        for i, line in enumerate(lines):
            data = json.loads(line)
            assert data["data"]["step_id"] == f"step-{i}"

    def test_get_results(self, store):
        """Test retrieving saved results."""
        # Save some results
        results = [
            StepResult(
                step_id=f"step-{i}",
                status=StepStatus.COMPLETED,
                content=f"Content {i}",
                attempt_count=1,
            )
            for i in range(3)
        ]
        
        for result in results:
            store.save_result(result)
        
        # Retrieve results
        retrieved = store.get_results()
        
        assert len(retrieved) == 3
        assert all(isinstance(r, StepResult) for r in retrieved)
        assert [r.step_id for r in retrieved] == ["step-0", "step-1", "step-2"]

    def test_get_results_empty_file(self, store):
        """Test getting results when file doesn't exist."""
        results = store.get_results()
        assert results == []

    def test_get_results_with_filter(self, store):
        """Test getting results with filtering."""
        # Save mixed results
        results = [
            StepResult(
                step_id="step-1",
                status=StepStatus.COMPLETED,
                content="Success",
                attempt_count=1,
            ),
            StepResult(
                step_id="step-2",
                status=StepStatus.FAILED,
                error="Error occurred",
                attempt_count=3,
            ),
            StepResult(
                step_id="step-3",
                status=StepStatus.COMPLETED,
                content="Another success",
                attempt_count=1,
            ),
        ]
        
        for result in results:
            store.save_result(result)
        
        # This would require implementing filtering in JSONLStore
        # For now, test that all results are returned
        retrieved = store.get_results()
        assert len(retrieved) == 3

    def test_save_state(self, store, sample_plan):
        """Test saving execution state."""
        state = ExecutionState(
            run_id="test-run",
            plan=sample_plan,
            status="running",
            completed_steps=["step1"],
        )
        
        store.save_state(state)
        
        # Read and verify
        with open(store.output_file, "r") as f:
            lines = f.readlines()
        
        assert len(lines) == 1
        
        saved_data = json.loads(lines[0])
        assert saved_data["type"] == "execution_state"
        assert saved_data["data"]["run_id"] == "test-run"
        assert saved_data["data"]["status"] == "running"
        assert saved_data["data"]["completed_steps"] == ["step1"]

    def test_get_latest_state(self, store, sample_plan):
        """Test retrieving the latest execution state."""
        # Save multiple states
        states = [
            ExecutionState(
                run_id="test-run",
                plan=sample_plan,
                status="running",
                completed_steps=[],
            ),
            ExecutionState(
                run_id="test-run",
                plan=sample_plan,
                status="running",
                completed_steps=["step1"],
            ),
            ExecutionState(
                run_id="test-run",
                plan=sample_plan,
                status="completed",
                completed_steps=["step1", "step2", "step3"],
            ),
        ]
        
        for state in states:
            store.save_state(state)
        
        # Get latest state
        latest = store.get_latest_state()
        
        assert latest is not None
        assert latest.status == "completed"
        assert len(latest.completed_steps) == 3

    def test_get_latest_state_no_states(self, store):
        """Test getting latest state when none exist."""
        state = store.get_latest_state()
        assert state is None

    def test_close(self, store):
        """Test closing the store."""
        # Mock the file handle
        mock_file = MagicMock()
        store._file = mock_file
        
        store.close()
        
        mock_file.close.assert_called_once()
        assert store._file is None

    def test_context_manager(self, temp_storage_dir):
        """Test using JSONLStore as a context manager."""
        with JSONLStore(storage_path=temp_storage_dir, run_id="test") as store:
            assert store._file is not None
            store.save_result(
                StepResult(
                    step_id="test",
                    status=StepStatus.COMPLETED,
                    content="Test",
                    attempt_count=1,
                )
            )
        
        # File should be closed after context
        assert store._file is None

    def test_save_with_special_characters(self, store):
        """Test saving results with special characters."""
        result = StepResult(
            step_id="test-step",
            status=StepStatus.COMPLETED,
            content='Content with "quotes" and \nnewlines',
            attempt_count=1,
        )
        
        store.save_result(result)
        
        # Should be able to read back
        retrieved = store.get_results()
        assert len(retrieved) == 1
        assert retrieved[0].content == 'Content with "quotes" and \nnewlines'

    def test_concurrent_writes(self, store):
        """Test that concurrent writes don't corrupt the file."""
        # This is a simple test - real concurrent testing would need threading
        results = []
        for i in range(10):
            result = StepResult(
                step_id=f"step-{i}",
                status=StepStatus.COMPLETED,
                content=f"Content {i}",
                attempt_count=1,
            )
            results.append(result)
            store.save_result(result)
        
        # All results should be retrievable
        retrieved = store.get_results()
        assert len(retrieved) == 10
        assert all(r.step_id == f"step-{i}" for i, r in enumerate(retrieved))

    def test_large_content(self, store):
        """Test saving results with large content."""
        # Create a large content string (1MB)
        large_content = "x" * (1024 * 1024)
        
        result = StepResult(
            step_id="large-step",
            status=StepStatus.COMPLETED,
            content=large_content,
            attempt_count=1,
        )
        
        store.save_result(result)
        
        # Should be able to read back
        retrieved = store.get_results()
        assert len(retrieved) == 1
        assert len(retrieved[0].content) == 1024 * 1024

    def test_malformed_jsonl_handling(self, store):
        """Test handling of malformed JSONL files."""
        # Write some valid and invalid lines
        with open(store.output_file, "w") as f:
            # Valid line
            f.write(json.dumps({
                "type": "step_result",
                "run_id": "test-run",
                "data": {
                    "step_id": "step-1",
                    "status": "completed",
                    "content": "Valid",
                    "attempt_count": 1,
                },
                "timestamp": datetime.utcnow().isoformat(),
            }) + "\n")
            
            # Invalid JSON
            f.write("This is not JSON\n")
            
            # Another valid line
            f.write(json.dumps({
                "type": "step_result",
                "run_id": "test-run",
                "data": {
                    "step_id": "step-2",
                    "status": "completed",
                    "content": "Also valid",
                    "attempt_count": 1,
                },
                "timestamp": datetime.utcnow().isoformat(),
            }) + "\n")
        
        # Should skip invalid lines and return valid ones
        results = store.get_results()
        assert len(results) == 2
        assert results[0].step_id == "step-1"
        assert results[1].step_id == "step-2"