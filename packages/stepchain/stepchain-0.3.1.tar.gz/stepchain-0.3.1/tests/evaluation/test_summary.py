#!/usr/bin/env python3
"""Quick summary of the evaluation test suite."""

import os
from pathlib import Path

def main():
    """Display test suite summary."""
    print("StepChain SDK Evaluation Test Suite")
    print("=" * 60)
    
    # Check environment
    api_key_set = bool(os.getenv("OPENAI_API_KEY"))
    print(f"\n✅ Environment:")
    print(f"  API Key: {'✓ Configured' if api_key_set else '❌ Not set'}")
    print(f"  Working Dir: {os.getcwd()}")
    
    # List test files
    print("\n📋 Test Files:")
    test_dir = Path(__file__).parent
    test_files = sorted(test_dir.glob("test_*.py"))
    
    for test_file in test_files:
        if test_file.name == "test_summary.py":
            continue
            
        # Read first few lines to get description
        with open(test_file) as f:
            lines = f.readlines()
            for line in lines[:10]:
                if line.strip().startswith('"""') and "Test" in line:
                    desc = line.strip().strip('"""')
                    print(f"  - {test_file.name}: {desc}")
                    break
    
    print("\n🚀 How to Run:")
    print("  1. Individual test: python tests/evaluation/test_1_basic_examples.py")
    print("  2. All tests: python tests/evaluation/run_all_tests.py")
    print("  3. With output: python tests/evaluation/test_1_basic_examples.py > output.txt 2>&1")
    
    print("\n📊 Expected Results:")
    print("  - Each test outputs PASS/FAIL status")
    print("  - Performance metrics (time, tokens)")
    print("  - Quality scores and comparisons")
    print("  - Detailed outputs saved to files")
    
    if not api_key_set:
        print("\n⚠️  WARNING: Set OPENAI_API_KEY before running tests:")
        print("  export OPENAI_API_KEY='your-key-here'")


if __name__ == "__main__":
    main()