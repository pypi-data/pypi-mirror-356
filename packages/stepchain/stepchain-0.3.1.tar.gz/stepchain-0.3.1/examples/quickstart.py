#!/usr/bin/env python3
"""Quick start example for StepChain."""

from stepchain import TaskDecomposer, Executor, setup_stepchain

def main():
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
    
    # Decompose the task
    plan = decomposer.decompose(task, tools=tools)
    print(f"\n✓ Created plan with {len(plan.steps)} steps:")
    
    for step in plan.steps:
        deps = f" (depends on: {', '.join(step.dependencies)})" if step.dependencies else ""
        print(f"  - {step.id}: {step.prompt[:60]}...{deps}")
    
    # Execute the plan
    print("\n🚀 Executing plan...")
    executor = Executor()
    
    try:
        results = executor.execute_plan(plan, run_id="healthcare_ai_analysis")
        
        # Show results
        successful = sum(1 for r in results if r.status.value == "completed")
        print(f"\n✓ Execution complete: {successful}/{len(results)} steps succeeded")
        
        # Display timing
        total_time = sum(r.duration_seconds or 0 for r in results)
        print(f"⏱️  Total execution time: {total_time:.2f} seconds")
        
    except Exception as e:
        print(f"\n❌ Execution failed: {e}")
        print("💡 Tip: You can resume this execution with:")
        print('    executor.execute_plan(plan, run_id="healthcare_ai_analysis", resume=True)')

if __name__ == "__main__":
    main()