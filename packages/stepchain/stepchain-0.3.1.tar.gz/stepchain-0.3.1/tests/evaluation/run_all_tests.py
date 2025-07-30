#!/usr/bin/env python3
"""Master test runner for StepChain evaluation tests."""

import os
import sys
import subprocess
import time
from pathlib import Path
from datetime import datetime

# Test modules
TEST_MODULES = [
    ("test_1_basic_examples.py", "Basic Examples Test"),
    ("test_2_complex_multi_tool.py", "Complex Multi-Tool Workflow"),
    ("test_3_failure_resume.py", "Failure and Resume Test"),
    ("test_4_performance_comparison.py", "Performance Comparison"),
    ("test_5_quality_assessment.py", "Quality Assessment")
]


def run_test(test_file: str, test_name: str) -> tuple[bool, str, float]:
    """Run a single test module."""
    print(f"\n{'='*70}")
    print(f"Running: {test_name}")
    print(f"File: {test_file}")
    print(f"{'='*70}")
    
    start_time = time.time()
    
    try:
        # Run the test
        result = subprocess.run(
            [sys.executable, test_file],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent
        )
        
        duration = time.time() - start_time
        
        # Check result
        success = result.returncode == 0
        
        # Capture output
        output = result.stdout
        if result.stderr:
            output += f"\n\nSTDERR:\n{result.stderr}"
        
        return success, output, duration
        
    except Exception as e:
        duration = time.time() - start_time
        return False, f"Error running test: {str(e)}", duration


def main():
    """Run all evaluation tests."""
    print("🚀 StepChain SDK Evaluation Test Suite")
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🐍 Python: {sys.version.split()[0]}")
    
    # Check environment
    if not os.getenv("OPENAI_API_KEY"):
        print("\n❌ ERROR: OPENAI_API_KEY environment variable not set")
        print("Please set your OpenAI API key before running tests:")
        print("  export OPENAI_API_KEY='your-api-key-here'")
        return 1
    
    print(f"✅ API Key configured")
    
    # Run all tests
    results = []
    total_start = time.time()
    
    for test_file, test_name in TEST_MODULES:
        success, output, duration = run_test(test_file, test_name)
        results.append({
            "name": test_name,
            "file": test_file,
            "success": success,
            "duration": duration,
            "output": output
        })
        
        # Save individual test output
        output_file = Path(f"output_{test_file.replace('.py', '.txt')}")
        with open(output_file, "w") as f:
            f.write(f"{test_name}\n")
            f.write(f"{'='*70}\n\n")
            f.write(output)
        
        print(f"\n{'✅ PASSED' if success else '❌ FAILED'} in {duration:.1f}s")
        print(f"Output saved to: {output_file}")
    
    total_duration = time.time() - total_start
    
    # Generate summary report
    print("\n" + "="*70)
    print("EVALUATION SUMMARY REPORT")
    print("="*70)
    
    passed = sum(1 for r in results if r["success"])
    total = len(results)
    
    print(f"\n📊 Overall Results: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    print(f"⏱️  Total Duration: {total_duration:.1f}s")
    
    print("\n📋 Test Results:")
    print("-" * 70)
    print(f"{'Test Name':<40} {'Status':<10} {'Duration':<10}")
    print("-" * 70)
    
    for result in results:
        status = "✅ PASS" if result["success"] else "❌ FAIL"
        print(f"{result['name']:<40} {status:<10} {result['duration']:.1f}s")
    
    # Key findings from outputs
    print("\n🔍 Key Findings:")
    
    # Check for specific patterns in outputs
    for result in results:
        if "Basic Examples" in result["name"] and result["success"]:
            if "steps succeeded" in result["output"]:
                print("  ✓ Basic quickstart example works correctly")
        
        if "Multi-Tool" in result["name"] and result["success"]:
            if "Tool Usage Distribution" in result["output"]:
                print("  ✓ Multi-tool workflows are properly supported")
        
        if "Failure and Resume" in result["name"] and result["success"]:
            if "Resume completed" in result["output"]:
                print("  ✓ Failure recovery and resume capability confirmed")
        
        if "Performance" in result["name"] and result["success"]:
            if "Time Overhead" in result["output"]:
                # Extract performance metrics
                lines = result["output"].split('\n')
                for line in lines:
                    if "Time Overhead:" in line:
                        print(f"  ℹ️  {line.strip()}")
                    if "Token Overhead:" in line:
                        print(f"  ℹ️  {line.strip()}")
        
        if "Quality" in result["name"] and result["success"]:
            if "Average Quality Scores:" in result["output"]:
                # Extract quality metrics
                lines = result["output"].split('\n')
                for i, line in enumerate(lines):
                    if "StepChain Approach:" in line:
                        print(f"  ✓ {line.strip()}")
                    if "Improvement:" in line and "points" in line:
                        print(f"  ✓ Quality {line.strip()}")
    
    # Generate final report
    report_path = Path("EVALUATION_REPORT.md")
    with open(report_path, "w") as f:
        f.write("# StepChain SDK Evaluation Report\n\n")
        f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Python Version:** {sys.version.split()[0]}\n")
        f.write(f"**Total Duration:** {total_duration:.1f}s\n\n")
        
        f.write("## Summary\n\n")
        f.write(f"- **Tests Passed:** {passed}/{total} ({passed/total*100:.1f}%)\n")
        f.write(f"- **Total Execution Time:** {total_duration:.1f}s\n\n")
        
        f.write("## Test Results\n\n")
        f.write("| Test | Status | Duration | Key Findings |\n")
        f.write("|------|--------|----------|-------------|\n")
        
        for result in results:
            status = "✅ PASS" if result["success"] else "❌ FAIL"
            
            # Extract key findings
            findings = []
            if "steps succeeded" in result["output"]:
                import re
                match = re.search(r'(\d+)/(\d+) steps succeeded', result["output"])
                if match:
                    findings.append(f"{match.group(1)}/{match.group(2)} steps")
            
            if "Quality Score:" in result["output"]:
                match = re.search(r'Quality Score: (\d+)/100', result["output"])
                if match:
                    findings.append(f"Quality: {match.group(1)}/100")
            
            findings_str = ", ".join(findings) if findings else "See output file"
            
            f.write(f"| {result['name']} | {status} | {result['duration']:.1f}s | {findings_str} |\n")
        
        f.write("\n## Conclusion\n\n")
        if passed == total:
            f.write("✅ **All tests passed successfully!** The StepChain SDK demonstrates:\n\n")
            f.write("- Reliable task decomposition and execution\n")
            f.write("- Robust failure handling and resume capability\n")
            f.write("- Support for multiple tool types (built-in, MCP, custom functions)\n")
            f.write("- Improved output quality compared to direct API calls\n")
            f.write("- Reasonable performance overhead for the benefits provided\n")
        else:
            f.write(f"⚠️  **{total - passed} test(s) failed.** Review the individual output files for details.\n")
        
        f.write("\n## Output Files\n\n")
        f.write("Detailed output for each test is available in:\n\n")
        for result in results:
            output_file = f"output_{result['file'].replace('.py', '.txt')}"
            f.write(f"- `{output_file}` - {result['name']}\n")
    
    print(f"\n📄 Full evaluation report saved to: {report_path}")
    
    # Exit code
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())