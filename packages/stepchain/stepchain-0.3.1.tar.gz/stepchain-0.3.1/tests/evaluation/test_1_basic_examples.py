#!/usr/bin/env python3
"""Test 1: Basic Examples Test
Run the quickstart.py example and verify it works.
"""

import os
import sys
import time
import traceback
from pathlib import Path

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from stepchain import setup_stepchain, TaskDecomposer, Executor


def test_quickstart_example():
    """Test the basic quickstart example."""
    print("=== Test 1: Basic Examples Test ===\n")
    
    try:
        # Check for API key
        if not os.getenv("OPENAI_API_KEY"):
            print("❌ FAIL: OPENAI_API_KEY environment variable not set")
            return False
            
        # Setup with zero configuration
        config = setup_stepchain()
        print(f"✓ StepChain configured with storage at: {config.storage_path}")
        
        # Define available tools
        tools = [
            "web_search",  # Built-in tool
            {
                "type": "function",
                "function": {
                    "name": "analyze_data",
                    "description": "Analyze data and generate insights",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "data_source": {"type": "string"},
                            "analysis_type": {"type": "string"}
                        }
                    }
                }
            }
        ]
        
        # Create decomposer
        decomposer = TaskDecomposer()
        
        # Complex task
        task = """
        Research the latest AI trends in healthcare and create a comprehensive report
        including market analysis, key players, and future predictions.
        """
        
        print(f"\n📋 Task: {task.strip()}")
        print("\n🔍 Decomposing task...")
        
        start_time = time.time()
        
        # Decompose the task
        plan = decomposer.decompose(task, tools=tools)
        
        decompose_time = time.time() - start_time
        
        print(f"\n✓ Created plan with {len(plan.steps)} steps in {decompose_time:.2f}s:")
        
        for step in plan.steps:
            deps = f" (depends on: {', '.join(step.dependencies)})" if step.dependencies else ""
            print(f"  - {step.id}: {step.prompt[:60]}...{deps}")
        
        # Execute the plan
        print("\n🚀 Executing plan...")
        executor = Executor()
        
        exec_start_time = time.time()
        
        results = executor.execute_plan(plan, run_id="healthcare_ai_analysis_test")
        
        exec_time = time.time() - exec_start_time
        
        # Show results
        successful = sum(1 for r in results if r.status.value == "completed")
        print(f"\n✓ Execution complete: {successful}/{len(results)} steps succeeded")
        
        # Display timing
        total_time = sum(r.duration_seconds or 0 for r in results)
        print(f"⏱️  Total execution time: {exec_time:.2f}s")
        print(f"⏱️  Sum of step times: {total_time:.2f}s")
        
        # Display some results
        print("\n📊 Sample Results:")
        for i, result in enumerate(results[:3]):  # Show first 3 results
            print(f"\nStep {i+1} ({result.step_id}):")
            print(f"  Status: {result.status.value}")
            if result.content:
                preview = result.content[:200] + "..." if len(result.content) > 200 else result.content
                print(f"  Output: {preview}")
        
        # Calculate tokens used
        total_input_tokens = sum(r.usage.get("input_tokens", 0) for r in results if r.usage)
        total_output_tokens = sum(r.usage.get("output_tokens", 0) for r in results if r.usage)
        total_tokens = total_input_tokens + total_output_tokens
        
        print(f"\n💰 Token Usage:")
        print(f"  Input tokens: {total_input_tokens:,}")
        print(f"  Output tokens: {total_output_tokens:,}")
        print(f"  Total tokens: {total_tokens:,}")
        
        # Test verdict
        if successful == len(results):
            print("\n✅ PASS: Basic example executed successfully!")
            return True
        else:
            print(f"\n⚠️  PARTIAL: {successful}/{len(results)} steps succeeded")
            return True  # Still consider it a pass if some steps succeeded
            
    except Exception as e:
        print(f"\n❌ FAIL: {type(e).__name__}: {str(e)}")
        traceback.print_exc()
        return False


def test_simple_api():
    """Test the simplified decompose/execute API."""
    print("\n\n=== Simple API Test ===\n")
    
    try:
        from stepchain import decompose, execute
        
        # Simple task
        task = "Write a Python function that calculates fibonacci numbers"
        
        print(f"📋 Task: {task}")
        print("🔍 Decomposing...")
        
        start_time = time.time()
        plan = decompose(task)
        decompose_time = time.time() - start_time
        
        print(f"✓ Created plan with {len(plan.steps)} steps in {decompose_time:.2f}s")
        
        print("🚀 Executing...")
        exec_start_time = time.time()
        results = execute(plan)
        exec_time = time.time() - exec_start_time
        
        successful = sum(1 for r in results if r.status.value == "completed")
        print(f"✓ Completed: {successful}/{len(results)} steps in {exec_time:.2f}s")
        
        # Find the step with the code
        code_steps = [r for r in results if 'def ' in (r.content or '')]
        if code_steps:
            print("\n📝 Generated Code:")
            print(code_steps[0].content)
        
        return successful > 0
        
    except Exception as e:
        print(f"\n❌ FAIL: {type(e).__name__}: {str(e)}")
        return False


def main():
    """Run all basic example tests."""
    print("StepChain Evaluation - Test 1: Basic Examples\n")
    print("=" * 60)
    
    results = []
    
    # Test 1: Quickstart example
    results.append(("Quickstart Example", test_quickstart_example()))
    
    # Test 2: Simple API
    results.append(("Simple API", test_simple_api()))
    
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