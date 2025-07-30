#!/usr/bin/env python3
"""Complex task decomposition and execution example.

This example shows how TaskCrew Segmenter handles a complex, multi-phase
task with parallel execution opportunities.
"""

import asyncio
from stepchain import (
    TaskDecomposer,
    AsyncExecutor,
)


async def market_analysis_example():
    """Complex example: Full market analysis for a new product launch."""
    
    print("=== Complex Task: Market Analysis for AI-Powered Fitness App ===\n")
    
    # Define the complex task
    task = """
    Conduct a comprehensive market analysis for launching a new AI-powered 
    fitness app in the US market, including:
    1. Market size and growth analysis
    2. Competitor analysis with feature comparison
    3. Target demographic research
    4. Pricing strategy recommendations
    5. Go-to-market strategy
    6. Financial projections and ROI analysis
    """
    
    # Create decomposer with maximum efficiency
    decomposer = TaskDecomposer(max_steps=20)
    
    # Define available tools for this analysis
    tools = [
        "web_search",
        "market_data_api",
        "competitor_analysis",
        "demographic_database",
        "financial_modeling",
        "data_visualization",
        "report_generator",
        "statistical_analysis",
    ]
    
    print("Decomposing complex task...")
    plan = decomposer.decompose(task, tools=tools)
    
    print(f"\nDecomposed into {len(plan.steps)} steps across multiple phases:")
    
    # Analyze the plan structure
    phases = {}
    for step in plan.steps:
        phase = step.metadata.get("phase", "general")
        if phase not in phases:
            phases[phase] = []
        phases[phase].append(step)
    
    for phase, steps in phases.items():
        print(f"\n{phase.upper()} ({len(steps)} steps):")
        for step in steps:
            deps = f" <- {', '.join(step.dependencies[:2])}..." if step.dependencies else ""
            print(f"  - {step.id}{deps}")
    
    # Calculate execution characteristics
    from stepchain import Scheduler
    scheduler = Scheduler()
    
    # Get execution waves
    completed = set()
    waves = []
    while len(completed) < len(plan.steps):
        ready = scheduler.get_ready_steps(plan, completed, set())
        if not ready:
            break
        wave_ids = [s.id for s in ready]
        waves.append(wave_ids)
        completed.update(wave_ids)
    
    print(f"\nExecution Analysis:")
    print(f"  - Total steps: {len(plan.steps)}")
    print(f"  - Execution waves: {len(waves)}")
    print(f"  - Max parallelization: {max(len(w) for w in waves)} concurrent steps")
    print(f"  - Critical path: {len(waves)} sequential stages")
    
    # Execute the plan asynchronously
    print("\n" + "="*50)
    print("Executing plan with async executor...")
    
    executor = AsyncExecutor(max_concurrent=5)
    
    # Add progress tracking
    from datetime import datetime
    start_time = datetime.now()
    
    results = await executor.execute_plan(plan, run_id="market_analysis_001")
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    # Analyze results
    completed_count = sum(1 for r in results if r.status.value == "completed")
    failed_count = sum(1 for r in results if r.status.value == "failed")
    
    print(f"\nExecution Summary:")
    print(f"  - Duration: {duration:.2f} seconds")
    print(f"  - Completed: {completed_count}/{len(results)} steps")
    print(f"  - Failed: {failed_count} steps")
    
    # Show sample outputs
    print("\nSample Outputs:")
    for result in results[:5]:
        if result.output and result.output.get("content"):
            content = result.output["content"][:150].replace("\n", " ")
            print(f"  {result.step_id}: {content}...")
    
    return plan, results


async def multi_task_decomposition():
    """Example decomposing multiple tasks."""
    
    print("\n=== Multi-Task Decomposition Example ===\n")
    
    # Create standard decomposer
    decomposer = TaskDecomposer()
    
    # Common task types
    tasks = [
        "Analyze customer churn data and identify key factors",
        "Research best practices for microservices architecture",
        "Create a social media content calendar for Q1 2024",
    ]
    
    for task in tasks:
        print(f"\nTask: {task}")
        plan = decomposer.decompose(task)
        print(f"Generated {len(plan.steps)} steps")
        
        # Show first few steps
        for step in plan.steps[:3]:
            print(f"  - {step.id}: {step.prompt[:60]}...")


async def decomposition_analysis_example():
    """Example analyzing decomposition characteristics."""
    
    print("\n=== Decomposition Analysis Example ===\n")
    
    task = "Build a recommendation system for an e-commerce platform"
    
    # Create decomposer with different max steps
    max_steps_options = [5, 10, 15]
    
    for max_steps in max_steps_options:
        print(f"\nMax Steps: {max_steps}")
        
        decomposer = TaskDecomposer(max_steps=max_steps)
        plan = decomposer.decompose(task)
        
        # Analyze characteristics
        deps_count = sum(len(s.dependencies) for s in plan.steps)
        avg_deps = deps_count / len(plan.steps) if plan.steps else 0
        
        print(f"  Steps: {len(plan.steps)}")
        print(f"  Avg dependencies: {avg_deps:.1f}")
        
        # Show execution pattern
        if len(plan.steps) <= 5:
            for step in plan.steps:
                deps = f" <- {', '.join(step.dependencies)}" if step.dependencies else ""
                print(f"    {step.id}{deps}")


async def error_handling_example():
    """Example showing error handling and retry behavior."""
    
    print("\n=== Error Handling Example ===\n")
    
    from stepchain import Plan, Step
    
    # Create a plan with a step that might fail
    plan = Plan(
        id="error_handling_demo",
        steps=[
            Step(
                id="unstable_api_call",
                prompt="Fetch data from unstable API endpoint",
                tools=["api_client"],
                max_retries=3,
            ),
            Step(
                id="process_data",
                prompt="Process the fetched data",
                dependencies=["unstable_api_call"],
            ),
        ]
    )
    
    # Execute with detailed logging
    import logging
    logging.basicConfig(level=logging.INFO)
    
    executor = AsyncExecutor()
    
    try:
        results = await executor.execute_plan(plan, run_id="error_demo_001")
        
        for result in results:
            print(f"\nStep: {result.step_id}")
            print(f"  Status: {result.status.value}")
            print(f"  Attempts: {result.attempt_count}")
            if result.error:
                print(f"  Error: {result.error}")
                print(f"  Error Type: {result.error_type.value if result.error_type else 'unknown'}")
    
    except Exception as e:
        print(f"Execution failed: {e}")


async def main():
    """Run all complex examples."""
    
    # Run market analysis example
    await market_analysis_example()
    
    # Run multi-task examples
    await multi_task_decomposition()
    
    # Run decomposition analysis
    await decomposition_analysis_example()
    
    # Run error handling example
    await error_handling_example()
    
    print("\n=== Complex Examples Complete ===")


if __name__ == "__main__":
    asyncio.run(main())