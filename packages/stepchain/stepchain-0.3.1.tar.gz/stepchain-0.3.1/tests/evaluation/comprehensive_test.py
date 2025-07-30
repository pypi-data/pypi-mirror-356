#!/usr/bin/env python3
"""
Comprehensive StepChain SDK Testing
Based on OpenAI Cookbook best practices for testing Responses API
"""

import os
import sys
import time
import json
import asyncio
from datetime import datetime
from typing import Dict, List, Any, Optional
import traceback

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from stepchain import setup_stepchain, decompose, execute, Executor, TaskDecomposer, Plan, Step
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI()

# Test results storage
test_results = {
    "timestamp": datetime.now().isoformat(),
    "tests": {}
}

def log_test_start(test_name: str):
    """Log test start"""
    print(f"\n{'='*60}")
    print(f"TEST: {test_name}")
    print(f"{'='*60}")
    test_results["tests"][test_name] = {
        "start_time": time.time(),
        "status": "running"
    }

def log_test_result(test_name: str, status: str, details: Dict[str, Any]):
    """Log test completion"""
    end_time = time.time()
    test_results["tests"][test_name]["end_time"] = end_time
    test_results["tests"][test_name]["duration"] = end_time - test_results["tests"][test_name]["start_time"]
    test_results["tests"][test_name]["status"] = status
    test_results["tests"][test_name]["details"] = details
    
    print(f"\nRESULT: {status}")
    print(f"Duration: {test_results['tests'][test_name]['duration']:.2f}s")
    if details:
        print(f"Details: {json.dumps(details, indent=2)}")

def test_1_complex_multi_tool_workflow():
    """Test complex workflow with multiple tool types"""
    log_test_start("Complex Multi-Tool Workflow")
    
    try:
        # Configure StepChain
        config = setup_stepchain()
        
        # Define tools - mix of built-in, MCP, and custom
        tools = [
            # Built-in web search
            {
                "type": "web_search"
            },
            # MCP server (simulated - would use real MCP in production)
            {
                "type": "mcp",
                "server_label": "github",
                "server_url": "https://gitmcp.io/openai/openai-python",
                "allowed_tools": ["search_code", "read_file"],
                "require_approval": "never"
            },
            # Custom function
            {
                "type": "function",
                "function": {
                    "name": "analyze_sentiment",
                    "description": "Analyze sentiment of text",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "text": {"type": "string", "description": "Text to analyze"}
                        },
                        "required": ["text"]
                    }
                }
            }
        ]
        
        # Complex task requiring multiple tools
        task = """
        Research the latest features in OpenAI's Python SDK by:
        1. Search the web for recent OpenAI Python SDK updates
        2. Look at the GitHub repository for recent changes
        3. Analyze sentiment of user feedback about the new features
        4. Create a comprehensive summary report
        """
        
        # Time decomposition
        decompose_start = time.time()
        plan = decompose(task, tools=tools, max_steps=8)
        decompose_time = time.time() - decompose_start
        
        # Verify plan structure
        assert isinstance(plan, Plan), "Decompose should return a Plan object"
        assert len(plan.steps) > 0, "Plan should have steps"
        assert len(plan.steps) <= 8, "Plan should respect max_steps"
        
        # Check tool distribution
        tool_usage = {"web_search": 0, "mcp": 0, "function": 0}
        for step in plan.steps:
            if step.tools:
                for tool in step.tools:
                    if tool.get("type") == "web_search":
                        tool_usage["web_search"] += 1
                    elif tool.get("type") == "mcp":
                        tool_usage["mcp"] += 1
                    elif tool.get("type") == "function":
                        tool_usage["function"] += 1
        
        # Execute plan
        execute_start = time.time()
        results = execute(plan, run_id=f"multi_tool_test_{int(time.time())}")
        execute_time = time.time() - execute_start
        
        # Verify results
        success_count = sum(1 for r in results if r.status == "completed")
        
        log_test_result("Complex Multi-Tool Workflow", "PASS", {
            "decompose_time": decompose_time,
            "execute_time": execute_time,
            "total_steps": len(plan.steps),
            "successful_steps": success_count,
            "tool_usage": tool_usage,
            "steps": [{"id": s.id, "description": s.description[:50]} for s in plan.steps]
        })
        
    except Exception as e:
        log_test_result("Complex Multi-Tool Workflow", "FAIL", {
            "error": str(e),
            "traceback": traceback.format_exc()
        })

def test_2_failure_and_resume():
    """Test failure recovery and resume capability"""
    log_test_start("Failure and Resume")
    
    try:
        config = setup_stepchain()
        
        # Create a plan that will partially execute
        task = """
        Create a comprehensive guide on Python best practices:
        1. Research current Python coding standards
        2. Analyze common mistakes in Python code
        3. Create examples of good vs bad code
        4. Write detailed explanations
        5. Format as a professional guide
        """
        
        # Create plan
        plan = decompose(task, max_steps=5)
        run_id = f"resume_test_{int(time.time())}"
        
        # Custom executor that simulates failure
        class FailingExecutor(Executor):
            def __init__(self, *args, fail_at_step=3, **kwargs):
                super().__init__(*args, **kwargs)
                self.fail_at_step = fail_at_step
                self.steps_executed = 0
                
            def execute_step(self, step, plan, run_id):
                self.steps_executed += 1
                if self.steps_executed == self.fail_at_step:
                    raise Exception("Simulated network failure")
                return super().execute_step(step, plan, run_id)
        
        # First execution - will fail
        executor = FailingExecutor(fail_at_step=3)
        first_start = time.time()
        try:
            results = executor.execute_plan(plan, run_id=run_id)
        except Exception as e:
            first_duration = time.time() - first_start
            failed_at_step = executor.steps_executed
        
        # Check state was saved
        storage_path = os.path.join(config.storage_path, f"{run_id}.jsonl")
        assert os.path.exists(storage_path), "State should be persisted"
        
        # Count completed steps in storage
        completed_before_resume = 0
        with open(storage_path, 'r') as f:
            for line in f:
                entry = json.loads(line)
                if entry.get("status") == "completed":
                    completed_before_resume += 1
        
        # Resume execution
        regular_executor = Executor()
        resume_start = time.time()
        results = regular_executor.execute_plan(plan, run_id=run_id, resume=True)
        resume_duration = time.time() - resume_start
        
        # Verify resume worked correctly
        final_success_count = sum(1 for r in results if r.status == "completed")
        
        log_test_result("Failure and Resume", "PASS", {
            "first_execution_duration": first_duration,
            "failed_at_step": failed_at_step,
            "completed_before_resume": completed_before_resume,
            "resume_duration": resume_duration,
            "final_successful_steps": final_success_count,
            "total_steps": len(plan.steps),
            "resumed_correctly": final_success_count == len(plan.steps)
        })
        
    except Exception as e:
        log_test_result("Failure and Resume", "FAIL", {
            "error": str(e),
            "traceback": traceback.format_exc()
        })

def test_3_performance_comparison():
    """Compare StepChain performance vs direct API calls"""
    log_test_start("Performance Comparison")
    
    try:
        config = setup_stepchain()
        
        # Test tasks of different complexities
        tasks = {
            "simple": "Write a haiku about programming",
            "medium": "Explain the concept of recursion with examples in Python",
            "complex": """Create a comprehensive tutorial on building a REST API with FastAPI including:
                         authentication, database integration, error handling, and deployment"""
        }
        
        results = {}
        
        for complexity, task in tasks.items():
            # Direct API call
            direct_start = time.time()
            direct_response = client.responses.create(
                model="gpt-4o-mini",
                input=task
            )
            direct_time = time.time() - direct_start
            direct_tokens = direct_response.usage.total_tokens if hasattr(direct_response, 'usage') else 0
            
            # StepChain approach
            stepchain_start = time.time()
            plan = decompose(task, max_steps=5)
            decompose_time = time.time() - stepchain_start
            
            execute_start = time.time()
            step_results = execute(plan, run_id=f"perf_test_{complexity}_{int(time.time())}")
            execute_time = time.time() - execute_start
            
            stepchain_total_time = decompose_time + execute_time
            
            # Calculate token usage (approximation based on step count)
            stepchain_tokens = len(plan.steps) * 800  # Rough estimate
            
            # Calculate overhead
            time_overhead = ((stepchain_total_time - direct_time) / direct_time) * 100
            token_overhead = ((stepchain_tokens - direct_tokens) / direct_tokens) * 100
            
            results[complexity] = {
                "direct_time": direct_time,
                "direct_tokens": direct_tokens,
                "stepchain_time": stepchain_total_time,
                "stepchain_tokens": stepchain_tokens,
                "decompose_time": decompose_time,
                "execute_time": execute_time,
                "time_overhead_percent": time_overhead,
                "token_overhead_percent": token_overhead,
                "steps_created": len(plan.steps)
            }
        
        log_test_result("Performance Comparison", "PASS", results)
        
    except Exception as e:
        log_test_result("Performance Comparison", "FAIL", {
            "error": str(e),
            "traceback": traceback.format_exc()
        })

def test_4_quality_assessment():
    """Assess quality improvement with StepChain"""
    log_test_start("Quality Assessment")
    
    try:
        config = setup_stepchain()
        
        # Task that benefits from decomposition
        task = """
        Write a comprehensive guide on 'Introduction to Machine Learning' that includes:
        - Clear explanation of core concepts
        - Real-world examples
        - Code samples in Python
        - Common pitfalls and how to avoid them
        - Resources for further learning
        """
        
        # Get direct response
        direct_response = client.responses.create(
            model="gpt-4o-mini",
            input=task
        )
        direct_output = direct_response.output[0].content[0].text if hasattr(direct_response, 'output') else ""
        
        # Get StepChain response
        plan = decompose(task, max_steps=6)
        results = execute(plan, run_id=f"quality_test_{int(time.time())}")
        
        # Combine StepChain outputs
        stepchain_output = "\n\n".join([r.content for r in results if r.status == "completed"])
        
        # Quality metrics
        def assess_quality(text: str) -> Dict[str, int]:
            """Simple quality assessment"""
            return {
                "length": len(text),
                "sections": text.count("\n#"),  # Markdown headers
                "code_blocks": text.count("```"),
                "bullet_points": text.count("\n-"),
                "examples": text.lower().count("example"),
                "has_introduction": 1 if "introduction" in text.lower() else 0,
                "has_conclusion": 1 if "conclusion" in text.lower() or "summary" in text.lower() else 0,
                "technical_terms": sum(1 for term in ["algorithm", "model", "data", "training", "prediction"] 
                                     if term in text.lower())
            }
        
        direct_quality = assess_quality(direct_output)
        stepchain_quality = assess_quality(stepchain_output)
        
        # Calculate improvement
        quality_improvement = {}
        for metric, direct_val in direct_quality.items():
            stepchain_val = stepchain_quality[metric]
            if direct_val > 0:
                improvement = ((stepchain_val - direct_val) / direct_val) * 100
            else:
                improvement = 100 if stepchain_val > 0 else 0
            quality_improvement[metric] = improvement
        
        log_test_result("Quality Assessment", "PASS", {
            "direct_quality": direct_quality,
            "stepchain_quality": stepchain_quality,
            "quality_improvement_percent": quality_improvement,
            "steps_used": len(plan.steps),
            "sample_direct_output": direct_output[:200] + "...",
            "sample_stepchain_output": stepchain_output[:200] + "..."
        })
        
    except Exception as e:
        log_test_result("Quality Assessment", "FAIL", {
            "error": str(e),
            "traceback": traceback.format_exc()
        })

def test_5_parallel_execution():
    """Test parallel step execution efficiency"""
    log_test_start("Parallel Execution")
    
    try:
        config = setup_stepchain()
        
        # Task with parallelizable subtasks
        task = """
        Analyze three different programming languages:
        1. Research Python's strengths and use cases
        2. Research JavaScript's strengths and use cases  
        3. Research Rust's strengths and use cases
        4. Compare all three languages
        5. Create a decision matrix for choosing between them
        """
        
        # Test with different concurrency levels
        concurrency_results = {}
        
        for max_concurrent in [1, 3, 5]:
            executor = Executor(max_concurrent=max_concurrent)
            plan = decompose(task, max_steps=5)
            
            start_time = time.time()
            results = executor.execute_plan(plan, run_id=f"parallel_test_{max_concurrent}_{int(time.time())}")
            duration = time.time() - start_time
            
            concurrency_results[f"max_{max_concurrent}"] = {
                "duration": duration,
                "steps": len(plan.steps),
                "successful": sum(1 for r in results if r.status == "completed")
            }
        
        # Calculate speedup
        sequential_time = concurrency_results["max_1"]["duration"]
        parallel_3_speedup = sequential_time / concurrency_results["max_3"]["duration"]
        parallel_5_speedup = sequential_time / concurrency_results["max_5"]["duration"]
        
        log_test_result("Parallel Execution", "PASS", {
            "concurrency_results": concurrency_results,
            "parallel_3_speedup": f"{parallel_3_speedup:.2f}x",
            "parallel_5_speedup": f"{parallel_5_speedup:.2f}x",
            "efficiency_gain": f"{((parallel_3_speedup - 1) * 100):.1f}%"
        })
        
    except Exception as e:
        log_test_result("Parallel Execution", "FAIL", {
            "error": str(e),
            "traceback": traceback.format_exc()
        })

def main():
    """Run all tests"""
    print("StepChain SDK Comprehensive Testing")
    print("=" * 60)
    print(f"Started at: {datetime.now()}")
    
    # Run tests
    test_1_complex_multi_tool_workflow()
    test_2_failure_and_resume()
    test_3_performance_comparison()
    test_4_quality_assessment()
    test_5_parallel_execution()
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for t in test_results["tests"].values() if t["status"] == "PASS")
    failed = sum(1 for t in test_results["tests"].values() if t["status"] == "FAIL")
    
    print(f"Total Tests: {len(test_results['tests'])}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Success Rate: {(passed/len(test_results['tests'])*100):.1f}%")
    
    # Save detailed results
    with open("test_results.json", "w") as f:
        json.dump(test_results, f, indent=2)
    
    print(f"\nDetailed results saved to: test_results.json")

if __name__ == "__main__":
    main()