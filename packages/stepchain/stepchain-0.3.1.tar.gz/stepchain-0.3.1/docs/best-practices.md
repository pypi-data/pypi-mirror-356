# StepChain Best Practices

## Table of Contents
- [Task Decomposition](#task-decomposition)
- [Tool Selection](#tool-selection)
- [Error Handling](#error-handling)
- [Performance Optimization](#performance-optimization)
- [Cost Management](#cost-management)
- [Production Deployment](#production-deployment)
- [Security Considerations](#security-considerations)
- [Debugging and Monitoring](#debugging-and-monitoring)

## Task Decomposition

### Write Clear, Specific Tasks

**✅ Good:**
```python
plan = decompose("""
    Analyze Q4 2023 sales data:
    1. Extract data from PostgreSQL (orders, customers tables)
    2. Calculate revenue by product category
    3. Compare with Q4 2022 for year-over-year growth
    4. Identify top 10 performing products
    5. Generate visualizations for executive presentation
""")
```

**❌ Bad:**
```python
plan = decompose("Do sales analysis")  # Too vague
```

### Set Reasonable Step Limits

```python
# For focused tasks
plan = decompose(task, max_steps=10)

# For complex workflows  
plan = decompose(task, max_steps=50)

# Never unlimited - always bound execution
```

### Include Success Criteria

```python
plan = decompose("""
    Optimize database performance:
    - Target: Reduce query time below 100ms
    - Constraint: No downtime during optimization
    - Success metric: 95th percentile query time
""")
```

## Tool Selection

### Use Built-in Tools When Possible

```python
# Prefer built-in tools
tools = ["web_search", "code_interpreter"]

# Over custom implementations
tools = [{
    "type": "function",
    "function": {"name": "my_search", ...},
    "implementation": my_search_function
}]
```

### MCP Server Best Practices

```python
# Good: Specific allowed tools
mcp_tool = {
    "type": "mcp",
    "server_label": "database",
    "server_url": "postgresql://db.company.com",
    "allowed_tools": ["read_only_query"],  # Restrict permissions
    "require_approval": "always"  # For production
}

# Bad: Overly permissive
mcp_tool = {
    "type": "mcp",
    "server_label": "database",
    "allowed_tools": ["*"],  # Dangerous!
    "require_approval": "never"
}
```

### Combine Tools Effectively

```python
# Complementary tool selection
tools = [
    "web_search",  # For external data
    {"type": "mcp", "server_label": "internal_db", ...},  # Internal data
    "code_interpreter",  # For analysis
    {"type": "function", "function": {...}, "implementation": validate_data}  # Validation
]
```

## Error Handling

### Always Use Run IDs for Critical Tasks

```python
# Good: Resumable execution
results = execute(plan, run_id="critical_analysis_20240115")

# Bad: No resume capability
results = execute(plan)  # Can't resume if it fails!
```

### Handle Partial Failures Gracefully

```python
results = execute(plan, run_id="data_pipeline")

# Check for failures
failed_steps = [r for r in results if r.status == "failed"]
if failed_steps:
    # Log failures
    for step in failed_steps:
        logger.error(f"Step {step.step_id} failed: {step.error}")
    
    # Decide whether to retry or alert
    if any("rate_limit" in str(step.error) for step in failed_steps):
        # Wait and retry
        time.sleep(60)
        results = execute(plan, run_id="data_pipeline", resume=True)
    else:
        # Alert for manual intervention
        send_alert("Pipeline failed - manual review needed")
```

### Implement Checkpoints for Long Tasks

```python
def execute_with_checkpoints(plan, run_id):
    """Execute with periodic status checks."""
    results = []
    
    # Start execution in background
    future = executor.submit(execute, plan, run_id)
    
    # Monitor progress
    while not future.done():
        # Check intermediate state
        state = storage.load_run_state(run_id)
        completed = len([r for r in state.results if r.status == "completed"])
        print(f"Progress: {completed}/{len(plan.steps)} steps")
        time.sleep(30)
    
    return future.result()
```

## Performance Optimization

### Optimize Parallelization

```python
# Adjust based on task type
executor = Executor(
    max_concurrent=5  # Good for I/O bound tasks (API calls)
)

executor = Executor(
    max_concurrent=1  # Good for CPU bound or sequential tasks
)
```

### Batch Operations

```python
# Good: Single decomposition for batch
plan = decompose("""
    Process customer list:
    1. Load all 1000 customers
    2. Validate data in batches of 100
    3. Enrich with external API (parallel)
    4. Generate summary report
""")

# Bad: Individual decomposition per item
for customer in customers:  # Don't do this!
    plan = decompose(f"Process customer {customer}")
```

### Cache Expensive Operations

```python
# Use MCP servers with caching
mcp_tool = {
    "type": "mcp",
    "server_label": "cached_api",
    "server_url": "https://api.company.com/mcp",
    "allowed_tools": ["get_data_cached"],
    "cache_ttl": 3600  # 1 hour cache
}
```

## Cost Management

### Set Token Limits

```python
# Control costs with temperature and max_steps
plan = decompose(
    task,
    temperature=0.2,  # Lower = more deterministic = fewer tokens
    max_steps=20  # Limit complexity
)
```

### Monitor API Usage

```python
class CostTracker:
    def __init__(self):
        self.total_tokens = 0
        self.cost_per_1k = 0.02  # GPT-4 pricing
    
    def track_execution(self, results):
        # Estimate tokens from results
        for result in results:
            self.total_tokens += len(str(result.output)) / 4  # Rough estimate
        
        cost = (self.total_tokens / 1000) * self.cost_per_1k
        print(f"Estimated cost: ${cost:.2f}")
```

### Use Appropriate Models

```python
# Complex reasoning tasks
plan = decompose(task, model="gpt-4")

# Simple tasks (when Responses API supports more models)
plan = decompose(task, model="gpt-3.5-turbo")
```

## Production Deployment

### Environment Configuration

```python
import os
from stepchain import setup_stepchain

# Production configuration
config = setup_stepchain(
    storage_path=os.getenv("STEPCHAIN_STORAGE", "/var/lib/stepchain"),
    log_level=os.getenv("STEPCHAIN_LOG_LEVEL", "WARNING")
)

# Validate configuration
assert os.getenv("OPENAI_API_KEY"), "OpenAI API key required"
```

### Implement Health Checks

```python
async def health_check():
    """Verify StepChain is operational."""
    try:
        # Test decomposition
        plan = decompose("Simple test task", max_steps=2)
        
        # Test execution
        results = execute(plan, run_id=f"health_check_{int(time.time())}")
        
        return {
            "status": "healthy",
            "decomposer": "ok",
            "executor": "ok",
            "storage": "ok"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }
```

### Implement Graceful Shutdown

```python
import signal
import sys

class ProductionExecutor:
    def __init__(self):
        self.executor = Executor()
        self.running_tasks = set()
        
        # Register signal handlers
        signal.signal(signal.SIGTERM, self.shutdown)
        signal.signal(signal.SIGINT, self.shutdown)
    
    def shutdown(self, signum, frame):
        """Graceful shutdown - save state before exit."""
        print("Shutting down gracefully...")
        
        # Wait for running tasks to checkpoint
        for task_id in self.running_tasks:
            print(f"Saving state for {task_id}")
            # State is automatically saved by StepChain
        
        sys.exit(0)
```

## Security Considerations

### Validate Tool Inputs

```python
def safe_database_tool(query: str) -> dict:
    """Validate queries before execution."""
    # Prevent destructive operations
    forbidden = ["DROP", "DELETE", "TRUNCATE", "UPDATE"]
    if any(word in query.upper() for word in forbidden):
        raise ValueError("Destructive operations not allowed")
    
    # Additional validation
    if not query.strip().upper().startswith("SELECT"):
        raise ValueError("Only SELECT queries allowed")
    
    return execute_query(query)
```

### Secure MCP Servers

```python
# Use authentication
mcp_tool = {
    "type": "mcp",
    "server_label": "secure_api",
    "server_url": "https://api.company.com/mcp",
    "env": {
        "API_KEY": os.getenv("SECURE_API_KEY"),  # Don't hardcode!
        "API_SECRET": os.getenv("SECURE_API_SECRET")
    }
}
```

### Audit Logging

```python
import logging
from datetime import datetime

class AuditedExecutor(Executor):
    def __init__(self, audit_logger):
        super().__init__()
        self.audit_logger = audit_logger
    
    async def execute_step(self, step, context):
        # Log before execution
        self.audit_logger.info({
            "timestamp": datetime.utcnow().isoformat(),
            "action": "step_start",
            "step_id": step.id,
            "tool": step.tool,
            "user": context.get("user_id")
        })
        
        result = await super().execute_step(step, context)
        
        # Log after execution
        self.audit_logger.info({
            "timestamp": datetime.utcnow().isoformat(),
            "action": "step_complete",
            "step_id": step.id,
            "status": result.status,
            "user": context.get("user_id")
        })
        
        return result
```

## Debugging and Monitoring

### Enable Verbose Logging

```python
import logging

# Development debugging
logging.getLogger("stepchain").setLevel(logging.DEBUG)

# Production - only errors
logging.getLogger("stepchain").setLevel(logging.ERROR)
```

### Implement Custom Monitoring

```python
from dataclasses import dataclass
from typing import Dict
import time

@dataclass
class ExecutionMetrics:
    total_steps: int = 0
    completed_steps: int = 0
    failed_steps: int = 0
    total_duration: float = 0
    step_durations: Dict[str, float] = None
    
    def success_rate(self):
        if self.total_steps == 0:
            return 0
        return self.completed_steps / self.total_steps

class MonitoredExecution:
    def __init__(self):
        self.metrics = ExecutionMetrics(step_durations={})
    
    def execute_with_metrics(self, plan, run_id):
        start_time = time.time()
        
        # Execute plan
        results = execute(plan, run_id=run_id)
        
        # Collect metrics
        self.metrics.total_steps = len(results)
        self.metrics.completed_steps = sum(1 for r in results if r.status == "completed")
        self.metrics.failed_steps = sum(1 for r in results if r.status == "failed")
        self.metrics.total_duration = time.time() - start_time
        
        # Step-level metrics
        for result in results:
            if result.completed_at and result.started_at:
                duration = (result.completed_at - result.started_at).total_seconds()
                self.metrics.step_durations[result.step_id] = duration
        
        # Send to monitoring system
        self.send_metrics()
        
        return results
    
    def send_metrics(self):
        # Send to Datadog, Prometheus, etc.
        print(f"Success rate: {self.metrics.success_rate():.2%}")
        print(f"Total duration: {self.metrics.total_duration:.1f}s")
```

### Debug Failed Steps

```python
def debug_failed_execution(run_id):
    """Analyze a failed execution."""
    storage = Storage()
    state = storage.load_run_state(run_id)
    
    print(f"Task: {state.plan.task_description}")
    print(f"Total steps: {len(state.plan.steps)}")
    
    # Analyze failures
    for result in state.results:
        if result.status == "failed":
            print(f"\nFailed step: {result.step_id}")
            print(f"Error: {result.error}")
            
            # Get step details
            step = next(s for s in state.plan.steps if s.id == result.step_id)
            print(f"Description: {step.description}")
            print(f"Tool: {step.tool}")
            print(f"Input: {step.tool_input}")
            print(f"Dependencies: {step.dependencies}")
            
            # Check if dependencies succeeded
            for dep_id in step.dependencies:
                dep_result = next((r for r in state.results if r.step_id == dep_id), None)
                if dep_result:
                    print(f"  Dependency {dep_id}: {dep_result.status}")
```

## Summary

### DO:
- ✅ Use run_ids for all production tasks
- ✅ Set reasonable step limits
- ✅ Monitor costs and performance
- ✅ Implement proper error handling
- ✅ Use built-in tools when possible
- ✅ Secure your MCP servers
- ✅ Test resume capability

### DON'T:
- ❌ Execute without run_ids in production
- ❌ Use unlimited max_steps
- ❌ Ignore failed steps
- ❌ Hardcode credentials
- ❌ Over-engineer simple tasks
- ❌ Add unnecessary abstractions

Remember: StepChain's philosophy is simplicity. If you're writing lots of code, you're probably doing it wrong.