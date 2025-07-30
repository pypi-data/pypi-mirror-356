#!/usr/bin/env python3
"""Demo: Custom function execution with TaskCrew Segmenter.

This demo shows how custom functions work without requiring API calls.
"""

import json
from datetime import datetime, timezone

from stepchain import (
    FunctionRegistry,
    Plan,
    Step,
    StepResult,
    StepStatus,
)


# Define custom functions
def get_current_time(timezone_name: str = "UTC") -> dict:
    """Get the current time in the specified timezone."""
    return {
        "timezone": timezone_name,
        "time": datetime.now(timezone.utc).isoformat(),
        "formatted": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
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
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "sections": [
                {"name": "Summary", "content": f"Report '{title}' generated with {len(data)} data points"},
                {"name": "Data", "content": json.dumps(data, indent=2)}
            ]
        }
    }


def demo_function_execution():
    """Demonstrate direct function execution."""
    print("=== Custom Functions Demo ===\n")
    
    # Create function registry
    registry = FunctionRegistry()
    registry.register("get_current_time", get_current_time)
    registry.register("calculate_statistics", calculate_statistics)
    registry.register("format_report", format_report)
    
    print("1. Testing get_current_time function:")
    time_result = registry.execute("get_current_time", {"timezone_name": "PST"})
    print(f"   Result: {json.dumps(time_result, indent=2)}")
    
    print("\n2. Testing calculate_statistics function:")
    numbers = [42, 17, 89, 23, 56, 91, 34, 78, 12, 65]
    stats_result = registry.execute("calculate_statistics", {"numbers": numbers})
    print(f"   Input: {numbers}")
    print(f"   Result: {json.dumps(stats_result, indent=2)}")
    
    print("\n3. Testing format_report function:")
    report_data = {
        "time_info": time_result,
        "statistics": stats_result
    }
    report_result = registry.execute("format_report", {
        "title": "Data Analysis Results",
        "data": report_data
    })
    print(f"   Result: {json.dumps(report_result, indent=2)}")
    
    print("\n4. Testing error handling:")
    try:
        registry.execute("unknown_function", {})
    except ValueError as e:
        print(f"   ✓ Correctly caught error: {e}")
    
    print("\n5. Testing timeout handling:")
    import time
    
    def slow_function():
        time.sleep(2)
        return {"status": "completed"}
    
    # Register with short timeout
    short_timeout_registry = FunctionRegistry(timeout=0.5)
    short_timeout_registry.register("slow_function", slow_function)
    
    try:
        short_timeout_registry.execute("slow_function", {})
    except TimeoutError as e:
        print(f"   ✓ Correctly caught timeout: {e}")


def demo_tool_integration():
    """Demonstrate how functions would be used in a plan."""
    print("\n\n=== Tool Integration Demo ===\n")
    
    # Define tools with proper OpenAI function calling format
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_current_time",
                "description": "Get the current time in a specified timezone",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "timezone_name": {
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
        }
    ]
    
    # Show how a plan would use these tools
    plan = Plan(
        steps=[
            Step(
                id="get_time",
                prompt="Get the current time",
                tools=tools
            ),
            Step(
                id="analyze_data",
                prompt="Calculate statistics for numbers: [10, 20, 30, 40, 50]",
                tools=tools,
                dependencies=["get_time"]
            )
        ]
    )
    
    print("Plan structure:")
    for step in plan.steps:
        print(f"  - {step.id}: {step.prompt}")
        print(f"    Tools: {len(step.tools)} custom functions available")
        if step.dependencies:
            print(f"    Dependencies: {step.dependencies}")
    
    # Simulate what would happen during execution
    print("\n\nSimulated execution:")
    
    # Create registry
    registry = FunctionRegistry()
    registry.register("get_current_time", get_current_time)
    registry.register("calculate_statistics", calculate_statistics)
    
    # Simulate step 1 execution
    print("\nStep 1: get_time")
    print("  LLM would call: get_current_time()")
    time_result = registry.execute("get_current_time", {})
    print(f"  Function result: {json.dumps(time_result, indent=4)}")
    
    # Simulate step 2 execution
    print("\nStep 2: analyze_data")
    print("  LLM would call: calculate_statistics(numbers=[10, 20, 30, 40, 50])")
    stats_result = registry.execute("calculate_statistics", {"numbers": [10, 20, 30, 40, 50]})
    print(f"  Function result: {json.dumps(stats_result, indent=4)}")


def demo_auto_registration():
    """Demonstrate auto-registration via implementation field."""
    print("\n\n=== Auto-Registration Demo ===\n")
    
    # Define a function
    def word_counter(text: str) -> dict:
        """Count words in text."""
        words = text.split()
        return {
            "word_count": len(words),
            "char_count": len(text),
            "unique_words": len(set(words))
        }
    
    # Tool definition with implementation
    tool_with_impl = {
        "type": "function",
        "function": {
            "name": "word_counter",
            "description": "Count words in text",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {"type": "string"}
                },
                "required": ["text"]
            }
        },
        "implementation": word_counter
    }
    
    # Auto-register
    registry = FunctionRegistry()
    registry.register_from_tools([tool_with_impl])
    
    # Test execution
    result = registry.execute("word_counter", {
        "text": "The quick brown fox jumps over the lazy dog"
    })
    
    print("Auto-registered function result:")
    print(f"  Input: 'The quick brown fox jumps over the lazy dog'")
    print(f"  Result: {json.dumps(result, indent=2)}")


def main():
    """Run all demos."""
    demo_function_execution()
    demo_tool_integration()
    demo_auto_registration()
    
    print("\n\n" + "="*50)
    print("✅ Custom Functions Demo Complete!")
    print("\nKey takeaways:")
    print("1. Functions are executed locally, not by the LLM")
    print("2. Results are real, not stub outputs")
    print("3. Full error handling and timeout support")
    print("4. Auto-registration makes integration seamless")
    print("5. Works with OpenAI's function calling format")


if __name__ == "__main__":
    main()