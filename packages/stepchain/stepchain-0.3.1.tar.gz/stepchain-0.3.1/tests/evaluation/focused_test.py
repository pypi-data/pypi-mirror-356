#!/usr/bin/env python3
"""
Focused StepChain SDK Testing - Grounded in actual execution
"""

import os
import sys
import time
import json
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from stepchain import setup_stepchain, decompose, execute
from openai import OpenAI

# Initialize
client = OpenAI()

print("StepChain SDK Focused Testing")
print("=" * 60)

# Test 1: Basic Functionality with Web Search
print("\n1. TESTING: Basic Web Search Integration")
print("-" * 40)

try:
    config = setup_stepchain()
    
    # Simple task with web search
    task = "Search for the latest OpenAI announcements and summarize them"
    tools = [{"type": "web_search"}]
    
    # Decompose
    start = time.time()
    plan = decompose(task, tools=tools, max_steps=3)
    decompose_time = time.time() - start
    
    print(f"✓ Decomposition successful in {decompose_time:.2f}s")
    print(f"  Steps created: {len(plan.steps)}")
    for i, step in enumerate(plan.steps):
        print(f"  Step {i+1}: {step.description[:60]}...")
    
    # Execute
    start = time.time()
    results = execute(plan, run_id=f"web_search_test_{int(time.time())}")
    execute_time = time.time() - start
    
    success_count = sum(1 for r in results if r.status == "completed")
    print(f"✓ Execution complete in {execute_time:.2f}s")
    print(f"  Successful steps: {success_count}/{len(plan.steps)}")
    
except Exception as e:
    print(f"✗ Test failed: {e}")

# Test 2: Performance Comparison
print("\n2. TESTING: Performance vs Direct API")
print("-" * 40)

try:
    task = "Explain what recursion is in programming"
    
    # Direct API call
    start = time.time()
    direct_response = client.responses.create(
        model="gpt-4o-mini",
        input=task
    )
    direct_time = time.time() - start
    direct_tokens = getattr(direct_response.usage, 'total_tokens', 0)
    
    # StepChain approach
    start = time.time()
    plan = decompose(task, max_steps=3)
    decompose_time = time.time() - start
    
    exec_start = time.time()
    results = execute(plan, run_id=f"perf_test_{int(time.time())}")
    execute_time = time.time() - exec_start
    
    stepchain_time = decompose_time + execute_time
    
    print(f"✓ Direct API: {direct_time:.2f}s ({direct_tokens} tokens)")
    print(f"✓ StepChain: {stepchain_time:.2f}s (decompose: {decompose_time:.2f}s, execute: {execute_time:.2f}s)")
    print(f"  Overhead: {((stepchain_time/direct_time - 1) * 100):.1f}%")
    print(f"  Steps used: {len(plan.steps)}")
    
except Exception as e:
    print(f"✗ Test failed: {e}")

# Test 3: State Persistence
print("\n3. TESTING: State Persistence and Resume")
print("-" * 40)

try:
    task = "Create a guide on Python decorators with examples"
    run_id = f"resume_test_{int(time.time())}"
    
    # Create and partially execute
    plan = decompose(task, max_steps=4)
    print(f"✓ Created plan with {len(plan.steps)} steps")
    
    # Check if state files are created
    storage_path = os.path.join(config.storage_path, f"{run_id}.jsonl")
    plan_path = os.path.join(config.storage_path, f"{run_id}_plan.json")
    
    # Execute first time
    results = execute(plan, run_id=run_id)
    
    # Verify persistence
    assert os.path.exists(storage_path), "State file not created"
    assert os.path.exists(plan_path), "Plan file not created"
    
    print(f"✓ State persisted to {storage_path}")
    
    # Count entries
    with open(storage_path, 'r') as f:
        entries = [json.loads(line) for line in f]
    completed = sum(1 for e in entries if e.get('status') == 'completed')
    
    print(f"✓ Completed steps saved: {completed}")
    
    # Test resume (should skip completed)
    start = time.time()
    results2 = execute(plan, run_id=run_id, resume=True)
    resume_time = time.time() - start
    
    print(f"✓ Resume executed in {resume_time:.2f}s (should be fast as all steps complete)")
    
except Exception as e:
    print(f"✗ Test failed: {e}")

# Test 4: Quality Check
print("\n4. TESTING: Output Quality")
print("-" * 40)

try:
    task = "Write a brief introduction to Python programming"
    
    # Direct response
    direct_resp = client.responses.create(model="gpt-4o-mini", input=task)
    direct_text = direct_resp.output[0].content[0].text if hasattr(direct_resp, 'output') else ""
    
    # StepChain response
    plan = decompose(task, max_steps=3)
    results = execute(plan, run_id=f"quality_test_{int(time.time())}")
    stepchain_text = "\n\n".join([r.content for r in results if r.status == "completed"])
    
    # Simple quality metrics
    direct_metrics = {
        "length": len(direct_text),
        "paragraphs": direct_text.count("\n\n"),
        "has_intro": "Python" in direct_text and "programming" in direct_text
    }
    
    stepchain_metrics = {
        "length": len(stepchain_text),
        "paragraphs": stepchain_text.count("\n\n"),
        "has_intro": "Python" in stepchain_text and "programming" in stepchain_text
    }
    
    print(f"✓ Direct output: {direct_metrics['length']} chars, {direct_metrics['paragraphs']} paragraphs")
    print(f"✓ StepChain output: {stepchain_metrics['length']} chars, {stepchain_metrics['paragraphs']} paragraphs")
    print(f"  Length increase: {((stepchain_metrics['length']/direct_metrics['length'] - 1) * 100):.1f}%")
    
except Exception as e:
    print(f"✗ Test failed: {e}")

# Summary
print("\n" + "="*60)
print("TEST SUMMARY")
print("="*60)
print("All tests completed. Check output above for results.")
print(f"Timestamp: {datetime.now()}")

# List all test outputs
print("\nTest artifacts created:")
for f in os.listdir(config.storage_path):
    if f.endswith('.jsonl') or f.endswith('.json'):
        size = os.path.getsize(os.path.join(config.storage_path, f))
        print(f"  - {f} ({size} bytes)")