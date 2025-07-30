#!/usr/bin/env python3
"""Example: Custom function execution with TaskCrew Segmenter.

This example shows how to register and use custom Python functions
as tools that can be executed during task execution.
"""

import asyncio
import json
from datetime import datetime

from stepchain import (
    Executor,
    FunctionRegistry,
    Plan,
    Step,
    setup_stepchain,
)


# Define custom functions
def get_current_time(timezone: str = "UTC") -> dict:
    """Get the current time in the specified timezone."""
    return {
        "timezone": timezone,
        "time": datetime.utcnow().isoformat(),
        "formatted": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    }


def calculate_statistics(numbers: list[float]) -> dict:
    """Calculate basic statistics for a list of numbers."""
    if not numbers:
        return {"error": "Empty list provided"}
    
    sorted_nums = sorted(numbers)
    n = len(numbers)
    
    return {
        "count": n,
        "sum": sum(numbers),
        "mean": sum(numbers) / n,
        "min": min(numbers),
        "max": max(numbers),
        "median": sorted_nums[n // 2] if n % 2 else (sorted_nums[n//2 - 1] + sorted_nums[n//2]) / 2,
        "range": max(numbers) - min(numbers)
    }


def format_report(title: str, data: dict) -> dict:
    """Format data into a structured report."""
    return {
        "report": {
            "title": title,
            "generated_at": datetime.utcnow().isoformat(),
            "sections": [
                {"name": "Summary", "content": f"Report '{title}' generated with {len(data)} data points"},
                {"name": "Data", "content": json.dumps(data, indent=2)}
            ]
        }
    }


async def main():
    """Run example with custom functions."""
    # Setup
    config = setup_stepchain()
    
    # Create function registry and register functions
    registry = FunctionRegistry()
    registry.register("get_current_time", get_current_time)
    registry.register("calculate_statistics", calculate_statistics)
    registry.register("format_report", format_report)
    
    # Define tools with custom functions
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_current_time",
                "description": "Get the current time in a specified timezone",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "timezone": {
                            "type": "string",
                            "description": "Timezone (e.g., UTC, EST, PST)",
                            "default": "UTC"
                        }
                    }
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "calculate_statistics",
                "description": "Calculate statistics for a list of numbers",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "numbers": {
                            "type": "array",
                            "items": {"type": "number"},
                            "description": "List of numbers to analyze"
                        }
                    },
                    "required": ["numbers"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "format_report",
                "description": "Format data into a structured report",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "Report title"
                        },
                        "data": {
                            "type": "object",
                            "description": "Data to include in the report"
                        }
                    },
                    "required": ["title", "data"]
                }
            }
        }
    ]
    
    # Create a plan that uses custom functions
    plan = Plan(
        steps=[
            Step(
                id="get_time",
                prompt="Get the current time using the get_current_time function",
                tools=tools
            ),
            Step(
                id="analyze_data",
                prompt="Calculate statistics for these numbers: [42, 17, 89, 23, 56, 91, 34, 78, 12, 65] using the calculate_statistics function",
                tools=tools,
                dependencies=["get_time"]
            ),
            Step(
                id="create_report",
                prompt="Create a report titled 'Data Analysis Results' that includes both the time information and statistics using the format_report function",
                tools=tools,
                dependencies=["get_time", "analyze_data"]
            )
        ]
    )
    
    # Execute with function registry
    executor = Executor(function_registry=registry)
    results = executor.execute_plan(plan, run_id="custom_functions_demo")
    
    # Display results
    print("\n=== Custom Functions Example Results ===\n")
    
    for result in results:
        print(f"Step: {result.step_id}")
        print(f"Status: {result.status}")
        
        if result.tool_calls:
            print("Tool Calls:")
            for tc in result.tool_calls:
                func_name = tc.get("function", {}).get("name", "unknown")
                print(f"  - {func_name}")
        
        if result.output and "tool_results" in result.output:
            print("Function Results:")
            for tool_id, output in result.output["tool_results"].items():
                print(f"  {tool_id}: {json.dumps(output, indent=4)}")
        
        print("-" * 50)
    
    print("\nNote: This example demonstrates how custom functions are executed")
    print("locally instead of relying on stub outputs!")


if __name__ == "__main__":
    asyncio.run(main())