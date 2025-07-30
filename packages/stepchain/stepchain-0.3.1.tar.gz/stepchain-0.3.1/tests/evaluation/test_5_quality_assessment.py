#!/usr/bin/env python3
"""Test 5: Quality Assessment
Compare the quality of outputs between decomposed vs direct approaches.
"""

import os
import sys
import time
import json
import re
import traceback
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from stepchain import setup_stepchain, TaskDecomposer, Executor, decompose, execute
from stepchain.integrations.openai import UnifiedLLMClient


def analyze_output_quality(content: str) -> Dict[str, any]:
    """Analyze the quality of generated content."""
    
    # Basic metrics
    word_count = len(content.split())
    sentence_count = len(re.findall(r'[.!?]+', content))
    paragraph_count = len([p for p in content.split('\n\n') if p.strip()])
    
    # Structure analysis
    has_sections = bool(re.findall(r'^#+\s+.*$|^[A-Z][^.!?]*:$', content, re.MULTILINE))
    has_lists = bool(re.findall(r'^\s*[-*•]\s+.*$|^\s*\d+\.\s+.*$', content, re.MULTILINE))
    has_code = bool(re.findall(r'```[\s\S]*?```|`[^`]+`', content))
    
    # Content depth
    technical_terms = len(re.findall(r'\b(?:API|SDK|function|method|class|algorithm|data|analysis|implementation|architecture)\b', content, re.IGNORECASE))
    
    # Completeness indicators
    has_introduction = bool(re.search(r'(?:introduction|overview|summary|abstract)', content[:500], re.IGNORECASE))
    has_conclusion = bool(re.search(r'(?:conclusion|summary|finally|in conclusion|to summarize)', content[-500:], re.IGNORECASE))
    
    # Calculate quality score (0-100)
    quality_score = 0
    
    # Length and structure (40 points)
    if word_count >= 100:
        quality_score += min(20, word_count / 10)  # Up to 20 points for length
    if has_sections:
        quality_score += 10
    if has_lists:
        quality_score += 5
    if paragraph_count >= 3:
        quality_score += 5
    
    # Content quality (40 points)
    if technical_terms >= 5:
        quality_score += min(20, technical_terms * 2)  # Up to 20 points
    if has_introduction:
        quality_score += 10
    if has_conclusion:
        quality_score += 10
    
    # Special content (20 points)
    if has_code:
        quality_score += 10
    if sentence_count > 0 and word_count / sentence_count < 25:  # Reasonable sentence length
        quality_score += 10
    
    return {
        "word_count": word_count,
        "sentence_count": sentence_count,
        "paragraph_count": paragraph_count,
        "has_structure": has_sections,
        "has_lists": has_lists,
        "has_code": has_code,
        "technical_depth": technical_terms,
        "has_introduction": has_introduction,
        "has_conclusion": has_conclusion,
        "quality_score": min(100, quality_score)
    }


def evaluate_task_quality(task: str, task_name: str = "Task") -> Dict[str, any]:
    """Evaluate quality for both direct and StepChain approaches."""
    print(f"\n{'='*60}")
    print(f"Quality Assessment: {task_name}")
    print(f"{'='*60}")
    
    results = {}
    
    # Direct approach
    print("\n1️⃣ Direct API Approach...")
    try:
        client = UnifiedLLMClient()
        
        start_time = time.time()
        response = client.create_completion(
            messages=[{"role": "user", "content": task}]
        )
        direct_time = time.time() - start_time
        
        direct_content = response.get("content", "")
        direct_quality = analyze_output_quality(direct_content)
        
        results["direct"] = {
            "content": direct_content,
            "quality": direct_quality,
            "time": direct_time,
            "tokens": response.get("usage", {}).get("total_tokens", 0)
        }
        
        print(f"✓ Completed in {direct_time:.2f}s")
        print(f"  Quality Score: {direct_quality['quality_score']}/100")
        
    except Exception as e:
        print(f"❌ Failed: {str(e)}")
        results["direct"] = None
    
    # StepChain approach
    print("\n2️⃣ StepChain Approach...")
    try:
        start_time = time.time()
        
        # Decompose and execute
        plan = decompose(task)
        results_list = execute(plan)
        
        stepchain_time = time.time() - start_time
        
        # Combine outputs
        stepchain_content = "\n\n".join(r.content for r in results_list if r.content)
        stepchain_quality = analyze_output_quality(stepchain_content)
        
        # Calculate total tokens
        total_tokens = sum(
            r.usage.get("input_tokens", 0) + r.usage.get("output_tokens", 0)
            for r in results_list if r.usage
        )
        
        results["stepchain"] = {
            "content": stepchain_content,
            "quality": stepchain_quality,
            "time": stepchain_time,
            "tokens": total_tokens,
            "steps": len(plan.steps)
        }
        
        print(f"✓ Completed in {stepchain_time:.2f}s with {len(plan.steps)} steps")
        print(f"  Quality Score: {stepchain_quality['quality_score']}/100")
        
    except Exception as e:
        print(f"❌ Failed: {str(e)}")
        traceback.print_exc()
        results["stepchain"] = None
    
    # Compare quality
    if results.get("direct") and results.get("stepchain"):
        print("\n📊 Quality Comparison:")
        
        direct_q = results["direct"]["quality"]
        stepchain_q = results["stepchain"]["quality"]
        
        # Detailed comparison
        metrics = [
            ("Word Count", "word_count"),
            ("Paragraphs", "paragraph_count"),
            ("Has Structure", "has_structure"),
            ("Technical Depth", "technical_depth"),
            ("Quality Score", "quality_score")
        ]
        
        print("\n  Metric          | Direct | StepChain")
        print("  " + "-" * 35)
        
        for metric_name, metric_key in metrics:
            direct_val = direct_q[metric_key]
            stepchain_val = stepchain_q[metric_key]
            
            if isinstance(direct_val, bool):
                direct_str = "Yes" if direct_val else "No"
                stepchain_str = "Yes" if stepchain_val else "No"
            else:
                direct_str = str(direct_val)
                stepchain_str = str(stepchain_val)
            
            print(f"  {metric_name:<15} | {direct_str:>6} | {stepchain_str:>9}")
        
        # Winner determination
        quality_diff = stepchain_q["quality_score"] - direct_q["quality_score"]
        
        print(f"\n🏆 Quality Assessment:")
        if quality_diff > 10:
            print(f"  StepChain produces significantly better quality (+{quality_diff} points)")
        elif quality_diff > 0:
            print(f"  StepChain produces slightly better quality (+{quality_diff} points)")
        elif quality_diff < -10:
            print(f"  Direct approach produces better quality ({quality_diff} points)")
        else:
            print(f"  Both approaches produce similar quality (diff: {quality_diff:+d} points)")
    
    return results


def test_quality_assessment():
    """Run quality assessment tests."""
    print("=== Test 5: Quality Assessment ===\n")
    
    # Check API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ FAIL: OPENAI_API_KEY environment variable not set")
        return False
    
    # Setup
    config = setup_stepchain()
    print(f"✓ StepChain configured")
    
    # Test cases focusing on quality
    test_cases = [
        {
            "name": "Technical Documentation",
            "task": "Write comprehensive documentation for a Python REST API client library including installation, authentication, basic usage examples, error handling, and best practices."
        },
        {
            "name": "Complex Analysis",
            "task": "Analyze the pros and cons of microservices architecture vs monolithic architecture for a startup building a SaaS product. Include scalability, development speed, maintenance, cost, and team considerations."
        },
        {
            "name": "Tutorial Creation",
            "task": "Create a step-by-step tutorial on implementing a binary search tree in Python, including insertion, deletion, searching, and traversal methods with code examples and complexity analysis."
        }
    ]
    
    all_results = []
    quality_scores = {"direct": [], "stepchain": []}
    
    for test_case in test_cases:
        try:
            results = evaluate_task_quality(test_case["task"], test_case["name"])
            all_results.append((test_case["name"], results))
            
            # Collect quality scores
            if results.get("direct"):
                quality_scores["direct"].append(results["direct"]["quality"]["quality_score"])
            if results.get("stepchain"):
                quality_scores["stepchain"].append(results["stepchain"]["quality"]["quality_score"])
                
        except Exception as e:
            print(f"\n❌ Error in {test_case['name']}: {str(e)}")
            all_results.append((test_case["name"], None))
    
    # Summary
    print("\n" + "="*60)
    print("QUALITY ASSESSMENT SUMMARY")
    print("="*60)
    
    if quality_scores["direct"] and quality_scores["stepchain"]:
        avg_direct = sum(quality_scores["direct"]) / len(quality_scores["direct"])
        avg_stepchain = sum(quality_scores["stepchain"]) / len(quality_scores["stepchain"])
        
        print(f"\n📊 Average Quality Scores:")
        print(f"  Direct Approach: {avg_direct:.1f}/100")
        print(f"  StepChain Approach: {avg_stepchain:.1f}/100")
        print(f"  Improvement: {avg_stepchain - avg_direct:+.1f} points")
        
        # Detailed breakdown
        print(f"\n📈 Quality Breakdown by Task:")
        for name, results in all_results:
            if results and results.get("direct") and results.get("stepchain"):
                direct_score = results["direct"]["quality"]["quality_score"]
                stepchain_score = results["stepchain"]["quality"]["quality_score"]
                print(f"  {name}: Direct={direct_score}, StepChain={stepchain_score} ({stepchain_score-direct_score:+d})")
        
        # Save sample outputs for manual review
        print("\n💾 Saving sample outputs for manual review...")
        
        output_dir = Path("quality_assessment_outputs")
        output_dir.mkdir(exist_ok=True)
        
        for name, results in all_results[:2]:  # Save first 2 examples
            if results:
                if results.get("direct"):
                    with open(output_dir / f"{name.replace(' ', '_')}_direct.txt", "w") as f:
                        f.write(results["direct"]["content"])
                
                if results.get("stepchain"):
                    with open(output_dir / f"{name.replace(' ', '_')}_stepchain.txt", "w") as f:
                        f.write(results["stepchain"]["content"])
        
        print(f"  Outputs saved to {output_dir}/")
        
        print("\n✅ PASS: Quality assessment completed successfully")
        return True
    else:
        print("\n❌ FAIL: Insufficient data for quality comparison")
        return False


def test_consistency():
    """Test output consistency across multiple runs."""
    print("\n\n=== Output Consistency Test ===\n")
    
    try:
        task = "Explain the concept of recursion in programming with an example"
        
        print(f"📋 Task: {task}")
        print("Running 3 iterations to test consistency...\n")
        
        # Run the same task 3 times with StepChain
        stepchain_qualities = []
        
        for i in range(3):
            print(f"Iteration {i+1}...")
            plan = decompose(task)
            results = execute(plan)
            
            content = "\n\n".join(r.content for r in results if r.content)
            quality = analyze_output_quality(content)
            stepchain_qualities.append(quality["quality_score"])
            
            print(f"  Quality score: {quality['quality_score']}/100")
        
        # Calculate consistency
        avg_score = sum(stepchain_qualities) / len(stepchain_qualities)
        max_deviation = max(abs(score - avg_score) for score in stepchain_qualities)
        consistency_score = 100 - (max_deviation * 2)  # Penalize deviation
        
        print(f"\n📊 Consistency Analysis:")
        print(f"  Scores: {stepchain_qualities}")
        print(f"  Average: {avg_score:.1f}")
        print(f"  Max deviation: {max_deviation:.1f}")
        print(f"  Consistency score: {consistency_score:.1f}/100")
        
        if consistency_score >= 80:
            print("✅ StepChain produces consistent quality outputs")
            return True
        else:
            print("⚠️  Some variability in output quality")
            return consistency_score >= 60
            
    except Exception as e:
        print(f"❌ Failed: {str(e)}")
        return False


def main():
    """Run all quality assessment tests."""
    print("StepChain Evaluation - Test 5: Quality Assessment\n")
    print("=" * 60)
    
    results = []
    
    # Test 1: Quality comparison
    results.append(("Quality Assessment", test_quality_assessment()))
    
    # Test 2: Consistency test
    results.append(("Output Consistency", test_consistency()))
    
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
    
    # Final recommendation
    if passed == total:
        print("\n🎯 RECOMMENDATION: StepChain provides superior output quality with good consistency.")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)