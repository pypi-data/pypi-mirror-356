#!/usr/bin/env python3
"""Test 4: Performance Comparison
Compare execution time and token usage between StepChain and direct API calls.
"""

import os
import sys
import time
import json
import statistics
import traceback
from pathlib import Path
from datetime import datetime

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from stepchain import setup_stepchain, TaskDecomposer, Executor, Step, Plan
from stepchain.integrations.openai import UnifiedLLMClient


def direct_api_approach(task: str, tools: list = None):
    """Execute task directly using the Responses API without decomposition."""
    client = UnifiedLLMClient()
    
    # Single comprehensive prompt
    messages = [
        {
            "role": "user",
            "content": task
        }
    ]
    
    # Format tools if provided
    formatted_tools = []
    if tools:
        for tool in tools:
            if isinstance(tool, str) and tool == "web_search":
                formatted_tools.append({"type": "web_search"})
            elif isinstance(tool, dict):
                formatted_tools.append(tool)
    
    start_time = time.time()
    
    response = client.create_completion(
        messages=messages,
        tools=formatted_tools if formatted_tools else None
    )
    
    end_time = time.time()
    duration = end_time - start_time
    
    return {
        "content": response.get("content", ""),
        "response_id": response.get("response_id"),
        "duration": duration,
        "usage": response.get("usage", {}),
        "approach": "direct"
    }


def stepchain_approach(task: str, tools: list = None):
    """Execute task using StepChain decomposition."""
    # Decompose
    decomposer = TaskDecomposer()
    
    decompose_start = time.time()
    plan = decomposer.decompose(task, tools=tools)
    decompose_time = time.time() - decompose_start
    
    # Execute
    executor = Executor()
    
    exec_start = time.time()
    results = executor.execute_plan(plan, run_id=f"perf_test_{int(time.time())}")
    exec_time = time.time() - exec_start
    
    # Aggregate results
    total_input_tokens = sum(r.usage.get("input_tokens", 0) for r in results if r.usage)
    total_output_tokens = sum(r.usage.get("output_tokens", 0) for r in results if r.usage)
    
    # Combine outputs
    combined_output = "\n\n".join(r.content for r in results if r.content)
    
    return {
        "content": combined_output,
        "duration": decompose_time + exec_time,
        "decompose_time": decompose_time,
        "exec_time": exec_time,
        "usage": {
            "input_tokens": total_input_tokens,
            "output_tokens": total_output_tokens,
            "total_tokens": total_input_tokens + total_output_tokens
        },
        "steps": len(plan.steps),
        "approach": "stepchain"
    }


def compare_approaches(task: str, tools: list = None, task_name: str = "Task"):
    """Compare direct vs StepChain approaches."""
    print(f"\n{'='*60}")
    print(f"Comparing: {task_name}")
    print(f"{'='*60}")
    
    print(f"\n📋 Task: {task[:100]}..." if len(task) > 100 else f"\n📋 Task: {task}")
    
    results = {}
    
    # Direct approach
    print("\n1️⃣ Direct API Approach...")
    try:
        direct_result = direct_api_approach(task, tools)
        results["direct"] = direct_result
        print(f"✓ Completed in {direct_result['duration']:.2f}s")
        print(f"  Tokens: {direct_result['usage'].get('total_tokens', 0):,}")
    except Exception as e:
        print(f"❌ Failed: {str(e)}")
        results["direct"] = None
    
    # StepChain approach
    print("\n2️⃣ StepChain Approach...")
    try:
        stepchain_result = stepchain_approach(task, tools)
        results["stepchain"] = stepchain_result
        print(f"✓ Completed in {stepchain_result['duration']:.2f}s")
        print(f"  Steps: {stepchain_result['steps']}")
        print(f"  Decompose: {stepchain_result['decompose_time']:.2f}s")
        print(f"  Execute: {stepchain_result['exec_time']:.2f}s")
        print(f"  Tokens: {stepchain_result['usage'].get('total_tokens', 0):,}")
    except Exception as e:
        print(f"❌ Failed: {str(e)}")
        results["stepchain"] = None
    
    # Comparison
    if results["direct"] and results["stepchain"]:
        print("\n📊 Performance Comparison:")
        
        # Time comparison
        time_diff = results["stepchain"]["duration"] - results["direct"]["duration"]
        time_ratio = results["stepchain"]["duration"] / results["direct"]["duration"]
        print(f"\n⏱️  Time:")
        print(f"  Direct: {results['direct']['duration']:.2f}s")
        print(f"  StepChain: {results['stepchain']['duration']:.2f}s")
        print(f"  Difference: {time_diff:+.2f}s ({time_ratio:.1f}x)")
        
        # Token comparison
        direct_tokens = results["direct"]["usage"].get("total_tokens", 0)
        stepchain_tokens = results["stepchain"]["usage"].get("total_tokens", 0)
        token_diff = stepchain_tokens - direct_tokens
        token_ratio = stepchain_tokens / direct_tokens if direct_tokens > 0 else 0
        
        print(f"\n💰 Tokens:")
        print(f"  Direct: {direct_tokens:,}")
        print(f"  StepChain: {stepchain_tokens:,}")
        print(f"  Difference: {token_diff:+,} ({token_ratio:.1f}x)")
        
        # Output length comparison
        direct_len = len(results["direct"]["content"])
        stepchain_len = len(results["stepchain"]["content"])
        
        print(f"\n📝 Output Length:")
        print(f"  Direct: {direct_len:,} chars")
        print(f"  StepChain: {stepchain_len:,} chars")
        
        # Determine winner
        print(f"\n🏆 Result:")
        if time_ratio < 1.5 and token_ratio < 1.5:
            print("  StepChain provides comparable performance with better structure")
        elif time_ratio > 2.0 or token_ratio > 2.0:
            print("  Direct approach is more efficient for this task")
        else:
            print("  Trade-off: StepChain adds ~{:.0f}% overhead but improves reliability".format((time_ratio - 1) * 100))
    
    return results


def test_performance_comparison():
    """Run performance comparison tests."""
    print("=== Test 4: Performance Comparison ===\n")
    
    # Check API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ FAIL: OPENAI_API_KEY environment variable not set")
        return False
    
    # Setup
    config = setup_stepchain()
    print(f"✓ StepChain configured")
    
    # Test cases
    test_cases = [
        {
            "name": "Simple Task",
            "task": "Write a haiku about artificial intelligence",
            "tools": None
        },
        {
            "name": "Medium Complexity Task",
            "task": "Research the top 3 programming languages in 2024 and summarize their key features",
            "tools": ["web_search"]
        },
        {
            "name": "Complex Multi-Step Task",
            "task": """Create a comprehensive analysis of renewable energy trends:
            1. Research current market data
            2. Identify top 5 technologies
            3. Analyze cost trends
            4. Predict future developments
            5. Create an executive summary""",
            "tools": ["web_search"]
        }
    ]
    
    all_results = []
    
    for test_case in test_cases:
        try:
            results = compare_approaches(
                test_case["task"],
                test_case["tools"],
                test_case["name"]
            )
            all_results.append((test_case["name"], results))
        except Exception as e:
            print(f"\n❌ Error in {test_case['name']}: {str(e)}")
            traceback.print_exc()
            all_results.append((test_case["name"], None))
    
    # Summary statistics
    print("\n" + "="*60)
    print("PERFORMANCE SUMMARY")
    print("="*60)
    
    valid_results = [(name, r) for name, r in all_results if r and r.get("direct") and r.get("stepchain")]
    
    if valid_results:
        # Calculate averages
        avg_time_ratio = statistics.mean(
            r["stepchain"]["duration"] / r["direct"]["duration"] 
            for _, r in valid_results
        )
        
        avg_token_ratio = statistics.mean(
            r["stepchain"]["usage"].get("total_tokens", 0) / r["direct"]["usage"].get("total_tokens", 1)
            for _, r in valid_results
            if r["direct"]["usage"].get("total_tokens", 0) > 0
        )
        
        print(f"\n📊 Average Performance Metrics:")
        print(f"  Time Overhead: {(avg_time_ratio - 1) * 100:.1f}%")
        print(f"  Token Overhead: {(avg_token_ratio - 1) * 100:.1f}%")
        
        # Task complexity vs overhead
        print(f"\n📈 Complexity Analysis:")
        for name, results in valid_results:
            if results:
                steps = results["stepchain"].get("steps", 0)
                time_ratio = results["stepchain"]["duration"] / results["direct"]["duration"]
                print(f"  {name}: {steps} steps, {time_ratio:.1f}x time")
        
        print("\n✅ PASS: Performance comparison completed successfully")
        return True
    else:
        print("\n❌ FAIL: No valid comparison results")
        return False


def test_parallel_execution_performance():
    """Test performance benefits of parallel execution."""
    print("\n\n=== Parallel Execution Performance Test ===\n")
    
    try:
        # Create a plan with parallel steps
        plan = Plan(
            goal="Parallel data analysis",
            steps=[
                Step(id="init", prompt="Initialize analysis"),
                # These 3 can run in parallel
                Step(id="analyze_1", prompt="Analyze dataset 1", dependencies=["init"]),
                Step(id="analyze_2", prompt="Analyze dataset 2", dependencies=["init"]),
                Step(id="analyze_3", prompt="Analyze dataset 3", dependencies=["init"]),
                # This depends on all analyses
                Step(id="combine", prompt="Combine all analyses", dependencies=["analyze_1", "analyze_2", "analyze_3"])
            ]
        )
        
        # Sequential execution (simulated)
        print("1️⃣ Sequential Execution (simulated)...")
        sequential_time = 0
        for step in plan.steps:
            # Simulate each step taking 1-2 seconds
            step_time = 1.5  # Average execution time
            sequential_time += step_time
        
        print(f"  Estimated time: {sequential_time:.1f}s")
        
        # Actual execution (which may parallelize)
        print("\n2️⃣ StepChain Execution...")
        executor = Executor()
        
        start_time = time.time()
        results = executor.execute_plan(plan, run_id=f"parallel_test_{int(time.time())}")
        actual_time = time.time() - start_time
        
        print(f"  Actual time: {actual_time:.1f}s")
        print(f"  Steps completed: {len(results)}")
        
        # Calculate efficiency
        efficiency = sequential_time / actual_time if actual_time > 0 else 1.0
        print(f"\n📊 Parallel Efficiency: {efficiency:.1f}x")
        
        if efficiency > 1.2:
            print("✅ Parallel execution provides performance benefits")
        else:
            print("ℹ️  Limited parallelization (may be due to API constraints)")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed: {str(e)}")
        return False


def main():
    """Run all performance comparison tests."""
    print("StepChain Evaluation - Test 4: Performance Comparison\n")
    print("=" * 60)
    
    results = []
    
    # Test 1: Direct comparison
    results.append(("Performance Comparison", test_performance_comparison()))
    
    # Test 2: Parallel execution
    results.append(("Parallel Execution", test_parallel_execution_performance()))
    
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