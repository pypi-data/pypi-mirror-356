#!/usr/bin/env python3
"""Basic usage example for TaskCrew Segmenter.

This example demonstrates the core functionality of task decomposition
and execution.
"""

import asyncio
import os
from stepchain import TaskDecomposer, Executor, AsyncExecutor


def basic_decomposition():
    """Example 1: Basic task decomposition."""
    print("=== Example 1: Basic Task Decomposition ===\n")
    
    # Create a decomposer
    decomposer = TaskDecomposer()
    
    # Decompose a task
    task = "Research competitors for a new productivity app and create a comparison report"
    plan = decomposer.decompose(task)
    
    print(f"Task: {task}")
    print(f"Decomposed into {len(plan.steps)} steps:\n")
    
    for i, step in enumerate(plan.steps, 1):
        deps = f" (depends on: {', '.join(step.dependencies)})" if step.dependencies else ""
        print(f"{i}. {step.id}{deps}")
        print(f"   Prompt: {step.prompt[:80]}...")
        print(f"   Tools: {', '.join(step.tools)}")
        print()
    
    return plan


def synchronous_execution(plan):
    """Example 2: Synchronous plan execution."""
    print("\n=== Example 2: Synchronous Execution ===\n")
    
    # Create an executor
    executor = Executor()
    
    # Execute the plan
    print("Executing plan synchronously...")
    results = executor.execute_plan(plan, run_id="example_sync_001")
    
    print(f"\nExecution completed. Results:")
    for result in results:
        status = "✓" if result.status.value == "completed" else "✗"
        print(f"{status} {result.step_id}: {result.status.value}")
        if result.output and result.output.get("content"):
            print(f"  Output preview: {result.output['content'][:100]}...")
    
    return results


async def asynchronous_execution(plan):
    """Example 3: Asynchronous plan execution with concurrency."""
    print("\n=== Example 3: Asynchronous Execution ===\n")
    
    # Create an async executor with max 3 concurrent steps
    executor = AsyncExecutor(max_concurrent=3)
    
    print("Executing plan asynchronously (max 3 concurrent steps)...")
    results = await executor.execute_plan(plan, run_id="example_async_001")
    
    print(f"\nExecution completed. Results:")
    for result in results:
        status = "✓" if result.status.value == "completed" else "✗"
        print(f"{status} {result.step_id}: {result.status.value}")
        if result.duration_seconds:
            print(f"  Duration: {result.duration_seconds:.2f}s")


def manual_plan_creation():
    """Example 4: Manual plan creation."""
    print("\n=== Example 4: Manual Plan Creation ===\n")
    
    from stepchain import Plan, Step
    
    # Create a plan manually
    plan = Plan(
        id="data_pipeline",
        steps=[
            Step(
                id="fetch_data",
                prompt="Fetch sales data from the API for Q4 2023",
                tools=["api_client", "data_parser"],
            ),
            Step(
                id="clean_data",
                prompt="Clean and validate the fetched data, handling missing values",
                tools=["python_code"],
                dependencies=["fetch_data"],
            ),
            Step(
                id="analyze_trends",
                prompt="Analyze sales trends and identify top-performing products",
                tools=["data_analysis", "statistical_tools"],
                dependencies=["clean_data"],
            ),
            Step(
                id="create_visualizations",
                prompt="Create charts showing sales trends and product performance",
                tools=["data_visualization"],
                dependencies=["analyze_trends"],
            ),
            Step(
                id="generate_report",
                prompt="Generate a comprehensive report with insights and recommendations",
                tools=["report_generator"],
                dependencies=["analyze_trends", "create_visualizations"],
            ),
        ]
    )
    
    print(f"Created plan '{plan.id}' with {len(plan.steps)} steps")
    
    # Validate the plan
    try:
        plan.validate_dependencies()
        print("✓ Plan validation passed")
    except ValueError as e:
        print(f"✗ Plan validation failed: {e}")
    
    return plan


def resume_execution():
    """Example 5: Resume a failed execution."""
    print("\n=== Example 5: Resume Failed Execution ===\n")
    
    from stepchain import JSONLStore
    
    # Check for existing runs
    store = JSONLStore()
    runs = store.list_runs()
    
    if not runs:
        print("No previous runs found to resume.")
        return
    
    print(f"Found {len(runs)} previous runs:")
    for run_id in runs[-5:]:  # Show last 5
        results = store.get_results(run_id)
        completed = sum(1 for r in results if r.status.value == "completed")
        print(f"  - {run_id}: {completed}/{len(results)} completed")
    
    # Example of resuming the last run
    if runs:
        last_run = runs[-1]
        print(f"\nResuming run: {last_run}")
        
        # Note: In a real scenario, you'd need to reconstruct the plan
        # or store it alongside the results


def main():
    """Run all examples."""
    # Check for API key
    if not os.environ.get("OPENAI_API_KEY"):
        print("Note: Set OPENAI_API_KEY environment variable for full functionality")
        print("Examples will use mock responses\n")
    
    # Run examples
    plan = basic_decomposition()
    
    # Only run execution examples if we have a small plan
    if len(plan.steps) <= 5:
        results = synchronous_execution(plan)
        asyncio.run(asynchronous_execution(plan))
    else:
        print("\nSkipping execution examples (plan too large for demo)")
    
    manual_plan = manual_plan_creation()
    resume_execution()
    
    print("\n=== Examples Complete ===")


if __name__ == "__main__":
    main()