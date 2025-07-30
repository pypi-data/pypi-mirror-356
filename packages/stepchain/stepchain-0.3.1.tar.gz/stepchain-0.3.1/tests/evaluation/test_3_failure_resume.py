#!/usr/bin/env python3
"""Test 3: Failure and Resume Test
Simulate a failure mid-execution and test resume capability.
"""

import os
import sys
import time
import json
import traceback
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from stepchain import (
    setup_stepchain,
    Executor,
    Plan,
    Step,
    StepStatus,
    JSONLStore
)


def test_failure_and_resume():
    """Test failure handling and resume capability."""
    print("=== Test 3: Failure and Resume Test ===\n")
    
    try:
        # Setup
        config = setup_stepchain()
        storage_path = config.storage_path
        print(f"✓ StepChain configured with storage at: {storage_path}")
        
        # Create a multi-step plan
        plan = Plan(
            goal="Multi-step data processing pipeline",
            steps=[
                Step(id="fetch_data", prompt="Fetch data from external source"),
                Step(id="validate_data", prompt="Validate the fetched data", dependencies=["fetch_data"]),
                Step(id="process_data", prompt="Process and transform the data", dependencies=["validate_data"]),
                Step(id="analyze_data", prompt="Analyze the processed data", dependencies=["process_data"]),
                Step(id="generate_report", prompt="Generate final report", dependencies=["analyze_data"])
            ]
        )
        
        print(f"📋 Created plan with {len(plan.steps)} steps")
        for step in plan.steps:
            deps = f" -> {', '.join(step.dependencies)}" if step.dependencies else ""
            print(f"  - {step.id}{deps}")
        
        run_id = "failure_resume_test"
        
        # First execution - simulate failure at step 3
        print("\n🚀 First execution (simulating failure at step 3)...")
        
        # Create executor with custom client to simulate failure
        executor = Executor()
        original_client = executor.client
        
        # Track execution
        execution_count = 0
        
        def mock_create_completion(**kwargs):
            nonlocal execution_count
            execution_count += 1
            
            if execution_count == 3:  # Fail on third step
                raise Exception("Simulated network error during process_data step")
            
            # Return normal response for other steps
            step_names = ["fetch_data", "validate_data", "process_data", "analyze_data", "generate_report"]
            step_name = step_names[execution_count - 1] if execution_count <= len(step_names) else "unknown"
            
            return {
                "content": f"Successfully completed {step_name}",
                "response_id": f"resp_{execution_count}",
                "usage": {
                    "input_tokens": 100,
                    "output_tokens": 50
                }
            }
        
        # Patch the client
        executor.client.create_completion = mock_create_completion
        
        # Execute and expect failure
        start_time = time.time()
        try:
            results = executor.execute_plan(plan, run_id=run_id)
            print("⚠️  Expected failure but execution succeeded")
        except Exception as e:
            exec_time = time.time() - start_time
            print(f"✓ Execution failed as expected after {exec_time:.2f}s: {str(e)}")
        
        # Check saved state
        print("\n📊 Checking saved state...")
        store = JSONLStore(base_path=storage_path)
        saved_results = store.get_results(run_id)
        
        print(f"Found {len(saved_results)} saved results:")
        for result in saved_results:
            status_icon = "✅" if result.status == StepStatus.COMPLETED else "❌"
            print(f"  {status_icon} {result.step_id}: {result.status.value}")
        
        # Verify expected state
        completed_steps = [r for r in saved_results if r.status == StepStatus.COMPLETED]
        failed_steps = [r for r in saved_results if r.status == StepStatus.FAILED]
        
        print(f"\nState summary:")
        print(f"  - Completed: {len(completed_steps)} steps")
        print(f"  - Failed: {len(failed_steps)} steps")
        
        if len(completed_steps) != 2 or len(failed_steps) != 1:
            print("❌ Unexpected state - expected 2 completed, 1 failed")
            return False
        
        # Second execution - resume from failure
        print("\n🔄 Resuming execution...")
        
        # Reset execution count and create new executor
        execution_count = 2  # Already executed 2 steps successfully
        executor2 = Executor()
        executor2.client.create_completion = mock_create_completion
        
        resume_start_time = time.time()
        results = executor2.execute_plan(plan, run_id=run_id, resume=True)
        resume_time = time.time() - resume_start_time
        
        print(f"✓ Resume completed in {resume_time:.2f}s")
        
        # Check final results
        print(f"\n📊 Final results: {len(results)} steps returned")
        
        # The executor returns only the newly executed steps when resuming
        for result in results:
            print(f"  - {result.step_id}: {result.status.value}")
            if result.content:
                print(f"    Output: {result.content}")
        
        # Verify all steps are now complete
        all_results = store.get_results(run_id)
        final_completed = [r for r in all_results if r.status == StepStatus.COMPLETED]
        
        print(f"\n✅ Final state: {len(final_completed)}/{len(plan.steps)} steps completed")
        
        # Test verdict
        if len(final_completed) == len(plan.steps):
            print("\n✅ PASS: Failure and resume test successful!")
            return True
        else:
            print(f"\n❌ FAIL: Expected all {len(plan.steps)} steps completed, got {len(final_completed)}")
            return False
            
    except Exception as e:
        print(f"\n❌ FAIL: {type(e).__name__}: {str(e)}")
        traceback.print_exc()
        return False


def test_multiple_failures():
    """Test handling multiple failures and retries."""
    print("\n\n=== Multiple Failures Test ===\n")
    
    try:
        # Setup
        config = setup_stepchain()
        
        # Simple plan
        plan = Plan(
            goal="Resilient data processing",
            steps=[
                Step(id="step1", prompt="First step"),
                Step(id="step2", prompt="Second step - will fail twice"),
                Step(id="step3", prompt="Third step")
            ]
        )
        
        run_id = "multiple_failures_test"
        
        # Track attempts
        step2_attempts = 0
        
        def mock_completion_with_retries(**kwargs):
            nonlocal step2_attempts
            
            # Identify which step based on prompt
            messages = kwargs.get("messages", [])
            prompt = messages[-1].get("content", "") if messages else ""
            
            if "Second step" in prompt:
                step2_attempts += 1
                if step2_attempts <= 2:  # Fail first 2 attempts
                    raise Exception(f"Simulated failure attempt {step2_attempts}")
            
            return {
                "content": f"Completed: {prompt[:30]}...",
                "response_id": f"resp_{time.time()}",
                "usage": {"input_tokens": 50, "output_tokens": 25}
            }
        
        # Execute with retries
        executor = Executor()
        executor.client.create_completion = mock_completion_with_retries
        
        print("🚀 Executing with automatic retries...")
        start_time = time.time()
        
        results = executor.execute_plan(plan, run_id=run_id)
        
        exec_time = time.time() - start_time
        
        successful = sum(1 for r in results if r.status == StepStatus.COMPLETED)
        print(f"✓ Execution complete: {successful}/{len(results)} steps in {exec_time:.2f}s")
        print(f"  Step 2 required {step2_attempts} attempts")
        
        return successful == len(plan.steps)
        
    except Exception as e:
        print(f"\n❌ FAIL: {type(e).__name__}: {str(e)}")
        return False


def test_partial_resume():
    """Test resuming with some steps already complete."""
    print("\n\n=== Partial Resume Test ===\n")
    
    try:
        config = setup_stepchain()
        
        # Create a plan with parallel branches
        plan = Plan(
            goal="Parallel processing with resume",
            steps=[
                Step(id="init", prompt="Initialize"),
                Step(id="branch_a1", prompt="Process branch A part 1", dependencies=["init"]),
                Step(id="branch_a2", prompt="Process branch A part 2", dependencies=["branch_a1"]),
                Step(id="branch_b1", prompt="Process branch B part 1", dependencies=["init"]),
                Step(id="branch_b2", prompt="Process branch B part 2", dependencies=["branch_b1"]),
                Step(id="merge", prompt="Merge results", dependencies=["branch_a2", "branch_b2"])
            ]
        )
        
        run_id = "partial_resume_test"
        
        # Manually save some completed steps to simulate partial execution
        store = JSONLStore(base_path=config.storage_path)
        store.save_plan(plan, run_id)
        
        # Simulate that init and branch_a1 are already done
        from stepchain.core.models import StepResult
        
        completed_results = [
            StepResult(
                step_id="init",
                status=StepStatus.COMPLETED,
                content="Initialized",
                response_id="resp_init",
                duration_seconds=1.0,
                usage={"input_tokens": 50, "output_tokens": 20}
            ),
            StepResult(
                step_id="branch_a1",
                status=StepStatus.COMPLETED,
                content="Branch A part 1 done",
                response_id="resp_a1",
                duration_seconds=1.5,
                usage={"input_tokens": 60, "output_tokens": 30}
            )
        ]
        
        for result in completed_results:
            store.save_result(result, run_id)
        
        print(f"📊 Pre-populated {len(completed_results)} completed steps")
        
        # Resume execution
        executor = Executor()
        
        # Simple mock that completes remaining steps
        def mock_remaining(**kwargs):
            messages = kwargs.get("messages", [])
            prompt = messages[-1].get("content", "") if messages else ""
            return {
                "content": f"Completed: {prompt[:40]}...",
                "response_id": f"resp_{time.time()}",
                "usage": {"input_tokens": 50, "output_tokens": 25}
            }
        
        executor.client.create_completion = mock_remaining
        
        print("🔄 Resuming execution...")
        results = executor.execute_plan(plan, run_id=run_id, resume=True)
        
        print(f"✓ Resumed and executed {len(results)} remaining steps")
        
        # Verify final state
        all_results = store.get_results(run_id)
        completed = sum(1 for r in all_results if r.status == StepStatus.COMPLETED)
        
        print(f"📊 Final state: {completed}/{len(plan.steps)} steps completed")
        
        return completed == len(plan.steps)
        
    except Exception as e:
        print(f"\n❌ FAIL: {type(e).__name__}: {str(e)}")
        traceback.print_exc()
        return False


def main():
    """Run all failure and resume tests."""
    print("StepChain Evaluation - Test 3: Failure and Resume\n")
    print("=" * 60)
    
    results = []
    
    # Test 1: Basic failure and resume
    results.append(("Failure and Resume", test_failure_and_resume()))
    
    # Test 2: Multiple failures with retries
    results.append(("Multiple Failures", test_multiple_failures()))
    
    # Test 3: Partial resume
    results.append(("Partial Resume", test_partial_resume()))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY:")
    print("=" * 60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)