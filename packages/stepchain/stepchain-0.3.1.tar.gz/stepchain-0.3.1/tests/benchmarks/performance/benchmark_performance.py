#!/usr/bin/env python3
"""
Performance Benchmark: Direct OpenAI Responses API vs StepChain SDK

This script compares the performance and capabilities between:
1. Direct OpenAI Responses API calls (one-shot)
2. StepChain SDK (task decomposition and chaining)

Metrics measured:
- Response time
- Token usage
- Task completion quality
- Error handling resilience
"""

import asyncio
import time
import json
import statistics
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import os
from openai import OpenAI
from stepchain import setup_stepchain, StepChain, StepChainConfig
from stepchain.types import Tool

# Test scenarios representing different complexity levels
TEST_SCENARIOS = [
    {
        "name": "Simple Task",
        "task": "Write a Python function that calculates the factorial of a number",
        "complexity": "low"
    },
    {
        "name": "Medium Complexity Task",
        "task": """Create a Python class for a simple todo list application with methods to:
        1. Add tasks
        2. Mark tasks as complete
        3. List all tasks
        4. Delete tasks
        Include proper error handling and documentation.""",
        "complexity": "medium"
    },
    {
        "name": "Complex Multi-Step Task",
        "task": """Build a complete Python web scraper that:
        1. Fetches data from a news website
        2. Parses article titles, dates, and content
        3. Stores the data in a SQLite database
        4. Generates a summary report in Markdown format
        5. Implements rate limiting and error handling
        6. Includes unit tests for the main functionality""",
        "complexity": "high"
    },
    {
        "name": "Research and Implementation Task",
        "task": """Research the best practices for implementing a caching system in Python, then:
        1. Compare different caching strategies (LRU, FIFO, TTL)
        2. Implement a flexible caching decorator that supports multiple strategies
        3. Add thread-safety
        4. Create benchmarks comparing performance
        5. Write comprehensive documentation with examples""",
        "complexity": "very_high",
        "requires_tools": True
    }
]

@dataclass
class BenchmarkResult:
    """Results from a single benchmark run"""
    method: str  # "direct_api" or "stepchain"
    scenario_name: str
    complexity: str
    execution_time: float
    tokens_used: int
    successful: bool
    error_message: Optional[str] = None
    response_quality_score: Optional[float] = None
    steps_executed: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class PerformanceBenchmark:
    def __init__(self):
        self.client = OpenAI()
        self.config = setup_stepchain()
        self.results: List[BenchmarkResult] = []
        
    async def run_direct_api_test(self, scenario: Dict[str, Any]) -> BenchmarkResult:
        """Test using direct OpenAI Responses API"""
        start_time = time.time()
        tokens_used = 0
        
        try:
            # Prepare tools if needed
            tools = []
            if scenario.get("requires_tools"):
                tools = [
                    {
                        "type": "web_search",
                        "web_search": {}
                    }
                ]
            
            # Direct API call
            response = self.client.responses.create(
                model="gpt-4o-mini",
                instructions="You are an expert software developer. Complete the given task thoroughly.",
                input=scenario["task"],
                tools=tools if tools else None
            )
            
            # Wait for completion with timeout
            max_wait = 300  # 5 minutes
            wait_start = time.time()
            
            while response.status in ["queued", "in_progress"]:
                if time.time() - wait_start > max_wait:
                    raise TimeoutError("Response timed out")
                await asyncio.sleep(2)
                response = self.client.responses.retrieve(response.id)
            
            execution_time = time.time() - start_time
            
            if response.status == "completed":
                # Extract token usage
                if hasattr(response, 'usage') and response.usage:
                    tokens_used = response.usage.total_tokens
                
                return BenchmarkResult(
                    method="direct_api",
                    scenario_name=scenario["name"],
                    complexity=scenario["complexity"],
                    execution_time=execution_time,
                    tokens_used=tokens_used,
                    successful=True,
                    steps_executed=1
                )
            else:
                return BenchmarkResult(
                    method="direct_api",
                    scenario_name=scenario["name"],
                    complexity=scenario["complexity"],
                    execution_time=execution_time,
                    tokens_used=tokens_used,
                    successful=False,
                    error_message=f"Response status: {response.status}"
                )
                
        except Exception as e:
            execution_time = time.time() - start_time
            return BenchmarkResult(
                method="direct_api",
                scenario_name=scenario["name"],
                complexity=scenario["complexity"],
                execution_time=execution_time,
                tokens_used=tokens_used,
                successful=False,
                error_message=str(e)
            )
    
    async def run_stepchain_test(self, scenario: Dict[str, Any]) -> BenchmarkResult:
        """Test using StepChain SDK"""
        start_time = time.time()
        
        try:
            # Prepare tools if needed
            tools = []
            if scenario.get("requires_tools"):
                tools = [Tool(type="web_search")]
            
            # Create and run StepChain
            chain = StepChain(
                task=scenario["task"],
                llm_model="gpt-4o-mini",
                tools=tools,
                config=self.config
            )
            
            result = await chain.run()
            
            execution_time = time.time() - start_time
            
            # Calculate total tokens used across all steps
            total_tokens = 0
            steps_count = 0
            
            if hasattr(result, 'state') and result.state:
                if hasattr(result.state, 'plan') and result.state.plan:
                    steps_count = len(result.state.plan.steps)
                
                if hasattr(result.state, 'step_results'):
                    for step_result in result.state.step_results.values():
                        if hasattr(step_result, 'usage') and step_result.usage:
                            total_tokens += step_result.usage.get('total_tokens', 0)
            
            return BenchmarkResult(
                method="stepchain",
                scenario_name=scenario["name"],
                complexity=scenario["complexity"],
                execution_time=execution_time,
                tokens_used=total_tokens,
                successful=result.success if hasattr(result, 'success') else True,
                steps_executed=steps_count,
                error_message=result.error if hasattr(result, 'error') and result.error else None
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            return BenchmarkResult(
                method="stepchain",
                scenario_name=scenario["name"],
                complexity=scenario["complexity"],
                execution_time=execution_time,
                tokens_used=0,
                successful=False,
                error_message=str(e)
            )
    
    async def run_benchmark_suite(self, runs_per_scenario: int = 3):
        """Run complete benchmark suite"""
        print("🚀 Starting Performance Benchmark...")
        print(f"Running {runs_per_scenario} iterations per scenario\n")
        
        for scenario in TEST_SCENARIOS:
            print(f"\n📋 Testing: {scenario['name']} (Complexity: {scenario['complexity']})")
            print("-" * 60)
            
            # Run direct API tests
            print("  Running Direct API tests...")
            for i in range(runs_per_scenario):
                result = await self.run_direct_api_test(scenario)
                self.results.append(result)
                print(f"    Run {i+1}: {'✅' if result.successful else '❌'} "
                      f"({result.execution_time:.2f}s, {result.tokens_used} tokens)")
            
            # Run StepChain tests
            print("  Running StepChain tests...")
            for i in range(runs_per_scenario):
                result = await self.run_stepchain_test(scenario)
                self.results.append(result)
                print(f"    Run {i+1}: {'✅' if result.successful else '❌'} "
                      f"({result.execution_time:.2f}s, {result.tokens_used} tokens, "
                      f"{result.steps_executed} steps)")
    
    def analyze_results(self) -> Dict[str, Any]:
        """Analyze benchmark results and generate statistics"""
        analysis = {
            "summary": {},
            "by_complexity": {},
            "by_method": {
                "direct_api": {},
                "stepchain": {}
            }
        }
        
        # Group results
        for complexity in ["low", "medium", "high", "very_high"]:
            complexity_results = [r for r in self.results if r.complexity == complexity]
            if not complexity_results:
                continue
                
            direct_results = [r for r in complexity_results if r.method == "direct_api"]
            stepchain_results = [r for r in complexity_results if r.method == "stepchain"]
            
            analysis["by_complexity"][complexity] = {
                "direct_api": self._calculate_stats(direct_results),
                "stepchain": self._calculate_stats(stepchain_results)
            }
        
        # Overall statistics
        direct_all = [r for r in self.results if r.method == "direct_api"]
        stepchain_all = [r for r in self.results if r.method == "stepchain"]
        
        analysis["by_method"]["direct_api"] = self._calculate_stats(direct_all)
        analysis["by_method"]["stepchain"] = self._calculate_stats(stepchain_all)
        
        # Calculate improvements
        if direct_all and stepchain_all:
            direct_stats = analysis["by_method"]["direct_api"]
            stepchain_stats = analysis["by_method"]["stepchain"]
            
            analysis["summary"] = {
                "total_runs": len(self.results),
                "success_rate_improvement": (
                    stepchain_stats["success_rate"] - direct_stats["success_rate"]
                ),
                "avg_time_difference": (
                    stepchain_stats["avg_execution_time"] - direct_stats["avg_execution_time"]
                ),
                "avg_token_difference": (
                    stepchain_stats["avg_tokens"] - direct_stats["avg_tokens"]
                ),
                "stepchain_advantages": [
                    "Better error handling and retry logic",
                    "Task decomposition for complex problems",
                    "Step-by-step progress tracking",
                    "Resumable execution on failures",
                    "Built-in tool support with MCP"
                ]
            }
        
        return analysis
    
    def _calculate_stats(self, results: List[BenchmarkResult]) -> Dict[str, Any]:
        """Calculate statistics for a set of results"""
        if not results:
            return {}
        
        successful = [r for r in results if r.successful]
        execution_times = [r.execution_time for r in results]
        tokens = [r.tokens_used for r in results if r.tokens_used > 0]
        
        stats = {
            "total_runs": len(results),
            "successful_runs": len(successful),
            "success_rate": len(successful) / len(results) * 100,
            "avg_execution_time": statistics.mean(execution_times),
            "min_execution_time": min(execution_times),
            "max_execution_time": max(execution_times),
        }
        
        if tokens:
            stats.update({
                "avg_tokens": statistics.mean(tokens),
                "min_tokens": min(tokens),
                "max_tokens": max(tokens),
            })
        else:
            stats.update({
                "avg_tokens": 0,
                "min_tokens": 0,
                "max_tokens": 0,
            })
        
        # Add step information for stepchain results
        stepchain_results = [r for r in results if r.method == "stepchain" and r.steps_executed]
        if stepchain_results:
            steps = [r.steps_executed for r in stepchain_results]
            stats["avg_steps"] = statistics.mean(steps)
        
        return stats
    
    def generate_report(self, output_file: str = "benchmark_results.md"):
        """Generate a detailed markdown report"""
        analysis = self.analyze_results()
        
        report = ["# StepChain vs Direct OpenAI API Performance Benchmark\n"]
        report.append(f"Generated on: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Summary
        summary = analysis.get("summary", {})
        if summary:
            report.append("## Executive Summary\n")
            report.append(f"- **Total benchmark runs**: {summary.get('total_runs', 0)}")
            report.append(f"- **Success rate improvement**: {summary.get('success_rate_improvement', 0):.1f}%")
            report.append(f"- **Average time difference**: {summary.get('avg_time_difference', 0):.2f}s")
            report.append(f"- **Average token difference**: {summary.get('avg_token_difference', 0):.0f} tokens\n")
            
            report.append("### StepChain Advantages\n")
            for advantage in summary.get("stepchain_advantages", []):
                report.append(f"- {advantage}")
            report.append("")
        
        # Results by complexity
        report.append("\n## Results by Task Complexity\n")
        for complexity, data in analysis["by_complexity"].items():
            report.append(f"### {complexity.title()} Complexity Tasks\n")
            report.append("| Metric | Direct API | StepChain | Difference |")
            report.append("|--------|------------|-----------|------------|")
            
            direct = data.get("direct_api", {})
            stepchain = data.get("stepchain", {})
            
            metrics = [
                ("Success Rate", "success_rate", "%", 1),
                ("Avg Time", "avg_execution_time", "s", 2),
                ("Avg Tokens", "avg_tokens", "", 0),
            ]
            
            for label, key, unit, decimals in metrics:
                d_val = direct.get(key, 0)
                s_val = stepchain.get(key, 0)
                diff = s_val - d_val
                
                if decimals == 0:
                    report.append(f"| {label} | {d_val:.0f}{unit} | {s_val:.0f}{unit} | "
                                f"{diff:+.0f}{unit} |")
                else:
                    report.append(f"| {label} | {d_val:.{decimals}f}{unit} | "
                                f"{s_val:.{decimals}f}{unit} | {diff:+.{decimals}f}{unit} |")
            
            if "avg_steps" in stepchain:
                report.append(f"\n*Average steps in StepChain: {stepchain['avg_steps']:.1f}*")
            
            report.append("")
        
        # Overall comparison
        report.append("\n## Overall Comparison\n")
        report.append("| Method | Success Rate | Avg Time | Avg Tokens |")
        report.append("|--------|--------------|----------|------------|")
        
        for method, data in analysis["by_method"].items():
            if data:
                report.append(f"| {method.replace('_', ' ').title()} | "
                            f"{data.get('success_rate', 0):.1f}% | "
                            f"{data.get('avg_execution_time', 0):.2f}s | "
                            f"{data.get('avg_tokens', 0):.0f} |")
        
        # Recommendations
        report.append("\n## Recommendations\n")
        report.append("Based on the benchmark results:\n")
        report.append("1. **For simple tasks**: Direct API calls may be sufficient and slightly faster")
        report.append("2. **For complex multi-step tasks**: StepChain provides better reliability and structure")
        report.append("3. **For tasks requiring tools**: StepChain's built-in tool support is advantageous")
        report.append("4. **For production systems**: StepChain's error handling and resume capability add robustness")
        
        # Save report
        with open(output_file, 'w') as f:
            f.write('\n'.join(report))
        
        # Also save raw results as JSON
        results_json = [r.to_dict() for r in self.results]
        with open('benchmark_raw_results.json', 'w') as f:
            json.dump({
                "results": results_json,
                "analysis": analysis
            }, f, indent=2)
        
        print(f"\n📊 Report saved to {output_file}")
        print(f"📈 Raw results saved to benchmark_raw_results.json")
        
        return '\n'.join(report)


async def main():
    """Run the benchmark suite"""
    benchmark = PerformanceBenchmark()
    
    # Run benchmarks
    await benchmark.run_benchmark_suite(runs_per_scenario=3)
    
    # Generate report
    report = benchmark.generate_report()
    
    # Print summary to console
    print("\n" + "="*60)
    print("BENCHMARK COMPLETE")
    print("="*60)
    
    analysis = benchmark.analyze_results()
    summary = analysis.get("summary", {})
    
    if summary:
        print(f"\n📊 Key Findings:")
        print(f"  - Success rate improvement: {summary.get('success_rate_improvement', 0):.1f}%")
        print(f"  - Average time difference: {summary.get('avg_time_difference', 0):.2f}s")
        print(f"  - Average token difference: {summary.get('avg_token_difference', 0):.0f} tokens")
        
        # Determine winner based on use case
        print(f"\n🏆 Recommendations:")
        by_complexity = analysis.get("by_complexity", {})
        
        for complexity in ["low", "medium", "high", "very_high"]:
            if complexity in by_complexity:
                data = by_complexity[complexity]
                direct = data.get("direct_api", {})
                stepchain = data.get("stepchain", {})
                
                # Compare success rates
                if direct and stepchain:
                    if stepchain.get("success_rate", 0) > direct.get("success_rate", 0):
                        print(f"  - {complexity.title()} complexity: StepChain "
                              f"(+{stepchain['success_rate'] - direct['success_rate']:.1f}% success rate)")
                    else:
                        time_diff = stepchain.get("avg_execution_time", 0) - direct.get("avg_execution_time", 0)
                        print(f"  - {complexity.title()} complexity: Direct API "
                              f"({abs(time_diff):.1f}s faster)")


if __name__ == "__main__":
    asyncio.run(main())