#!/usr/bin/env python3
"""Test 2: Complex Multi-Tool Workflow
Test that uses web_search, MCP servers, and custom functions together.
"""

import os
import sys
import time
import json
import traceback
from pathlib import Path
from datetime import datetime

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from stepchain import (
    setup_stepchain,
    TaskDecomposer,
    Executor,
    FunctionRegistry,
    Plan,
    Step
)


# Custom functions for the test
def analyze_sentiment(text: str) -> dict:
    """Analyze sentiment of text."""
    positive_words = ["good", "great", "excellent", "amazing", "positive", "successful"]
    negative_words = ["bad", "terrible", "awful", "poor", "negative", "failed"]
    
    text_lower = text.lower()
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)
    
    if positive_count > negative_count:
        sentiment = "positive"
        score = positive_count / (positive_count + negative_count) if negative_count > 0 else 1.0
    elif negative_count > positive_count:
        sentiment = "negative"
        score = negative_count / (positive_count + negative_count) if positive_count > 0 else 1.0
    else:
        sentiment = "neutral"
        score = 0.5
    
    return {
        "sentiment": sentiment,
        "confidence": score,
        "positive_words": positive_count,
        "negative_words": negative_count,
        "analysis_timestamp": datetime.utcnow().isoformat()
    }


def summarize_data(data: list, max_items: int = 5) -> dict:
    """Summarize a list of data items."""
    if not data:
        return {"summary": "No data provided", "count": 0}
    
    return {
        "summary": f"Analyzed {len(data)} items",
        "count": len(data),
        "sample": data[:max_items],
        "truncated": len(data) > max_items
    }


def calculate_metrics(values: list[float]) -> dict:
    """Calculate statistical metrics."""
    if not values:
        return {"error": "No values provided"}
    
    sorted_vals = sorted(values)
    n = len(values)
    
    return {
        "count": n,
        "mean": sum(values) / n,
        "min": min(values),
        "max": max(values),
        "median": sorted_vals[n // 2] if n % 2 else (sorted_vals[n//2 - 1] + sorted_vals[n//2]) / 2,
        "range": max(values) - min(values)
    }


def test_complex_multi_tool_workflow():
    """Test a complex workflow using multiple tool types."""
    print("=== Test 2: Complex Multi-Tool Workflow ===\n")
    
    try:
        # Setup
        config = setup_stepchain()
        print(f"✓ StepChain configured")
        
        # Create function registry
        registry = FunctionRegistry()
        registry.register("analyze_sentiment", analyze_sentiment)
        registry.register("summarize_data", summarize_data)
        registry.register("calculate_metrics", calculate_metrics)
        
        # Define all tool types
        tools = [
            # Built-in tool
            "web_search",
            
            # MCP servers (simulated - would need real endpoints in production)
            {
                "type": "mcp",
                "server_label": "database",
                "server_url": "postgresql://localhost:5432/mcp",
                "allowed_tools": ["query_data", "analyze_schema"],
                "require_approval": "never"
            },
            {
                "type": "mcp",
                "server_label": "analytics",
                "server_url": "https://analytics.example.com/mcp",
                "allowed_tools": ["get_metrics", "create_report"],
                "require_approval": "never"
            },
            
            # Custom functions
            {
                "type": "function",
                "function": {
                    "name": "analyze_sentiment",
                    "description": "Analyze sentiment of text content",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "text": {"type": "string", "description": "Text to analyze"}
                        },
                        "required": ["text"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "summarize_data",
                    "description": "Summarize a collection of data",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "data": {"type": "array", "description": "Data to summarize"},
                            "max_items": {"type": "integer", "description": "Maximum items to include", "default": 5}
                        },
                        "required": ["data"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "calculate_metrics",
                    "description": "Calculate statistical metrics",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "values": {
                                "type": "array",
                                "items": {"type": "number"},
                                "description": "Numeric values to analyze"
                            }
                        },
                        "required": ["values"]
                    }
                }
            }
        ]
        
        # Complex task that requires multiple tools
        task = """
        Perform a comprehensive analysis of customer feedback:
        1. Search the web for recent customer reviews about AI products
        2. Analyze sentiment of the reviews
        3. Query our database for internal customer feedback data
        4. Calculate statistical metrics on satisfaction scores
        5. Create a comprehensive report combining all findings
        """
        
        print(f"📋 Complex Task: {task.strip()}\n")
        
        # Decompose
        decomposer = TaskDecomposer()
        print("🔍 Decomposing complex task...")
        
        start_time = time.time()
        plan = decomposer.decompose(task, tools=tools)
        decompose_time = time.time() - start_time
        
        print(f"✓ Created plan with {len(plan.steps)} steps in {decompose_time:.2f}s")
        
        # Analyze tool usage in the plan
        tool_usage = {}
        for step in plan.steps:
            print(f"\n  Step: {step.id}")
            print(f"  Task: {step.prompt[:80]}...")
            if step.tools:
                print(f"  Tools: {len(step.tools)} tool(s)")
                for tool in step.tools:
                    if isinstance(tool, str):
                        tool_name = tool
                    elif isinstance(tool, dict):
                        tool_name = tool.get("type", "unknown")
                        if tool_name == "mcp":
                            tool_name = f"mcp:{tool.get('server_label', 'unknown')}"
                        elif tool_name == "function":
                            tool_name = f"function:{tool.get('function', {}).get('name', 'unknown')}"
                    else:
                        tool_name = "unknown"
                    
                    tool_usage[tool_name] = tool_usage.get(tool_name, 0) + 1
            if step.dependencies:
                print(f"  Dependencies: {', '.join(step.dependencies)}")
        
        print("\n📊 Tool Usage Distribution:")
        for tool, count in sorted(tool_usage.items()):
            print(f"  - {tool}: {count} step(s)")
        
        # Execute
        print("\n🚀 Executing complex multi-tool plan...")
        executor = Executor(function_registry=registry)
        
        exec_start_time = time.time()
        results = executor.execute_plan(plan, run_id="complex_multi_tool_test")
        exec_time = time.time() - exec_start_time
        
        # Results
        successful = sum(1 for r in results if r.status.value == "completed")
        print(f"\n✓ Execution complete: {successful}/{len(results)} steps succeeded in {exec_time:.2f}s")
        
        # Analyze results
        print("\n📈 Execution Analysis:")
        
        # Tool execution tracking
        tool_executions = {}
        for result in results:
            if result.tool_calls:
                for tool_call in result.tool_calls:
                    tool_type = tool_call.get("type", "unknown")
                    if tool_type == "function":
                        tool_name = f"function:{tool_call.get('function', {}).get('name', 'unknown')}"
                    else:
                        tool_name = tool_type
                    
                    tool_executions[tool_name] = tool_executions.get(tool_name, 0) + 1
        
        if tool_executions:
            print("\nTools Actually Executed:")
            for tool, count in sorted(tool_executions.items()):
                print(f"  - {tool}: {count} execution(s)")
        
        # Token usage
        total_input_tokens = sum(r.usage.get("input_tokens", 0) for r in results if r.usage)
        total_output_tokens = sum(r.usage.get("output_tokens", 0) for r in results if r.usage)
        
        print(f"\n💰 Token Usage:")
        print(f"  Input tokens: {total_input_tokens:,}")
        print(f"  Output tokens: {total_output_tokens:,}")
        print(f"  Total tokens: {total_input_tokens + total_output_tokens:,}")
        
        # Show sample outputs
        print("\n📄 Sample Outputs:")
        for i, result in enumerate(results[:3]):
            if result.content:
                print(f"\nStep {i+1} ({result.step_id}):")
                preview = result.content[:150] + "..." if len(result.content) > 150 else result.content
                print(f"  {preview}")
        
        # Test verdict
        if successful >= len(results) * 0.8:  # 80% success rate
            print("\n✅ PASS: Complex multi-tool workflow executed successfully!")
            return True
        else:
            print(f"\n⚠️  PARTIAL: {successful}/{len(results)} steps succeeded")
            return successful > 0
            
    except Exception as e:
        print(f"\n❌ FAIL: {type(e).__name__}: {str(e)}")
        traceback.print_exc()
        return False


def test_manual_multi_tool_plan():
    """Test manually created plan with multiple tools."""
    print("\n\n=== Manual Multi-Tool Plan Test ===\n")
    
    try:
        # Setup
        registry = FunctionRegistry()
        registry.register("analyze_sentiment", analyze_sentiment)
        registry.register("calculate_metrics", calculate_metrics)
        
        # Create manual plan
        plan = Plan(
            goal="Analyze market sentiment and metrics",
            steps=[
                Step(
                    id="search_news",
                    prompt="Search for recent AI market news and trends",
                    tools=["web_search"]
                ),
                Step(
                    id="analyze_sentiment",
                    prompt="Analyze the sentiment of the news: 'AI market shows strong growth with positive investor sentiment'",
                    tools=[{
                        "type": "function",
                        "function": {
                            "name": "analyze_sentiment",
                            "description": "Analyze sentiment",
                            "parameters": {
                                "type": "object",
                                "properties": {"text": {"type": "string"}},
                                "required": ["text"]
                            }
                        }
                    }],
                    dependencies=["search_news"]
                ),
                Step(
                    id="calculate_metrics",
                    prompt="Calculate metrics for values: [85.2, 92.1, 88.5, 91.3, 87.9]",
                    tools=[{
                        "type": "function",
                        "function": {
                            "name": "calculate_metrics",
                            "description": "Calculate metrics",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "values": {"type": "array", "items": {"type": "number"}}
                                },
                                "required": ["values"]
                            }
                        }
                    }],
                    dependencies=["search_news"]
                ),
                Step(
                    id="combine_analysis",
                    prompt="Combine sentiment analysis and metrics into a final report",
                    dependencies=["analyze_sentiment", "calculate_metrics"]
                )
            ]
        )
        
        print(f"📋 Created manual plan with {len(plan.steps)} steps")
        
        # Execute
        executor = Executor(function_registry=registry)
        results = executor.execute_plan(plan, run_id="manual_multi_tool_test")
        
        successful = sum(1 for r in results if r.status.value == "completed")
        print(f"✓ Completed: {successful}/{len(results)} steps")
        
        return successful >= 3  # At least 3 out of 4 steps should succeed
        
    except Exception as e:
        print(f"\n❌ FAIL: {type(e).__name__}: {str(e)}")
        return False


def main():
    """Run all complex multi-tool tests."""
    print("StepChain Evaluation - Test 2: Complex Multi-Tool Workflow\n")
    print("=" * 60)
    
    results = []
    
    # Test 1: Complex decomposed workflow
    results.append(("Complex Multi-Tool Workflow", test_complex_multi_tool_workflow()))
    
    # Test 2: Manual multi-tool plan
    results.append(("Manual Multi-Tool Plan", test_manual_multi_tool_plan()))
    
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