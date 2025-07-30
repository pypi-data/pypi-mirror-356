#!/usr/bin/env python3
"""Ultra-simple StepChain example - 10x developer style."""

from stepchain import decompose
from stepchain import Executor

# That's it. Two imports.

def main():
    # 1. Decompose any task in one line
    plan = decompose("Build a web scraper for hackernews")
    
    # 2. Execute it
    executor = Executor()
    results = executor.execute_plan(plan, run_id="simple_demo")
    
    # 3. Done
    print(f"Completed {len([r for r in results if r.status.value == 'completed'])} steps")

# Even simpler - coming soon:
# from stepchain import run
# run("Build a web scraper for hackernews")

if __name__ == "__main__":
    main()