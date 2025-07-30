#!/usr/bin/env python3
"""
MCP Server Integration Example

This example demonstrates how to integrate MCP (Model Context Protocol) servers
with StepChain for powerful, production-ready AI workflows.

MCP servers provide a standardized way to connect LLMs to external services,
databases, and APIs. StepChain makes it trivial to use them.
"""

import asyncio
from stepchain import decompose, execute, setup_stepchain
from stepchain.core import Executor

# Example 1: Basic MCP Server Usage
def basic_mcp_example():
    """Connect to a single MCP server for GitHub operations."""
    print("\n=== Example 1: Basic MCP Server ===")
    
    # Define an MCP tool - connects to GitHub via MCP
    github_mcp = {
        "type": "mcp",
        "server_label": "github",
        "server_url": "https://github.mcp.com/myorg/myrepo",
        "allowed_tools": ["search_code", "read_file", "create_issue"],
        "require_approval": "never"  # or "always" for manual approval
    }
    
    # Decompose task with MCP tool
    plan = decompose(
        "Find all Python files with TODO comments and create GitHub issues for them",
        tools=[github_mcp]
    )
    
    # Execute with automatic retry and state persistence
    results = execute(plan, run_id="github_todos")
    
    print(f"Completed {sum(1 for r in results if r.status == 'completed')}/{len(results)} steps")


# Example 2: Multiple MCP Servers
def multi_mcp_example():
    """Orchestrate across multiple MCP servers."""
    print("\n=== Example 2: Multiple MCP Servers ===")
    
    tools = [
        # Database MCP server
        {
            "type": "mcp",
            "server_label": "postgres",
            "server_url": "postgresql://localhost:5432/analytics",
            "allowed_tools": ["query", "analyze_schema", "export_data"],
        },
        # Slack MCP server
        {
            "type": "mcp",
            "server_label": "slack",
            "server_url": "https://slack.com/api/mcp/workspace",
            "allowed_tools": ["send_message", "read_channel", "upload_file"],
        },
        # Also use built-in tools
        "web_search",
        "code_interpreter"
    ]
    
    plan = decompose(
        """Analyze this week's sales data:
        1. Query sales database for weekly metrics
        2. Compare with last week and last year
        3. Generate visualizations
        4. Post insights to #sales-team Slack channel
        """,
        tools=tools
    )
    
    # Execute with custom configuration
    executor = Executor(max_concurrent=3)
    results = executor.execute_plan(plan, run_id="weekly_sales_analysis")
    
    # Check for any failures
    failed = [r for r in results if r.status == "failed"]
    if failed:
        print(f"Warning: {len(failed)} steps failed")
        for r in failed:
            print(f"  - Step {r.step_id}: {r.error}")


# Example 3: MCP + Custom Functions
def mcp_with_custom_functions():
    """Combine MCP servers with your own Python functions."""
    print("\n=== Example 3: MCP + Custom Functions ===")
    
    # Your custom analysis function
    def calculate_growth_rate(current: float, previous: float) -> dict:
        """Calculate growth rate with additional metrics."""
        growth = ((current - previous) / previous) * 100
        return {
            "growth_rate": round(growth, 2),
            "absolute_change": current - previous,
            "multiplier": round(current / previous, 2)
        }
    
    tools = [
        # Financial data MCP server
        {
            "type": "mcp",
            "server_label": "financial_api",
            "server_url": "https://api.financial.com/mcp/v1",
            "allowed_tools": ["get_stock_price", "get_financials", "get_news"],
        },
        # Your custom function
        {
            "type": "function",
            "function": {
                "name": "calculate_growth_rate",
                "description": "Calculate growth rate between two values",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "current": {"type": "number", "description": "Current value"},
                        "previous": {"type": "number", "description": "Previous value"}
                    },
                    "required": ["current", "previous"]
                }
            },
            "implementation": calculate_growth_rate
        }
    ]
    
    plan = decompose(
        "Analyze Apple's revenue growth over the last 4 quarters",
        tools=tools
    )
    
    results = execute(plan, run_id="aapl_growth_analysis")


# Example 4: Production MCP Setup with Error Handling
async def production_mcp_example():
    """Production-ready MCP integration with monitoring."""
    print("\n=== Example 4: Production MCP Setup ===")
    
    # Initialize with configuration
    config = setup_stepchain()
    
    # Production MCP tools with monitoring
    tools = [
        {
            "type": "mcp",
            "server_label": "production_db",
            "server_url": "postgresql://prod.db.company.com:5432/main",
            "allowed_tools": ["read_only_query"],  # Restrict to safe operations
            "require_approval": "always",  # Manual approval for production
            "timeout": 30,  # Timeout for safety
        },
        {
            "type": "mcp",
            "server_label": "monitoring",
            "server_url": "https://monitoring.company.com/mcp",
            "allowed_tools": ["log_metric", "create_alert"],
        }
    ]
    
    # Complex production task
    task = """
    Perform daily customer health check:
    1. Query active customers from last 30 days
    2. Calculate engagement metrics per customer
    3. Identify customers with declining usage
    4. Generate personalized re-engagement emails
    5. Log metrics to monitoring system
    6. Create alerts for customers needing immediate attention
    """
    
    plan = decompose(task, tools=tools, model="gpt-4")
    
    # Execute with resume capability
    run_id = "daily_health_check_2024_01_15"
    
    try:
        results = execute(plan, run_id=run_id)
        
        # Log success metrics
        completed = sum(1 for r in results if r.status == "completed")
        print(f"Health check completed: {completed}/{len(results)} steps successful")
        
    except Exception as e:
        print(f"Execution interrupted: {e}")
        print("Resuming from last checkpoint...")
        
        # Resume from exact point of failure
        results = execute(plan, run_id=run_id, resume=True)
        print("Health check resumed and completed")


# Example 5: Real Python MCP Server Implementation
def python_mcp_server_example():
    """Example using actual Python MCP servers from the ecosystem."""
    print("\n=== Example 5: Real Python MCP Servers ===")
    
    # Example with popular Python MCP servers
    tools = [
        # Git operations via MCP
        {
            "type": "mcp",
            "server_label": "git",
            "server_command": "uvx",  # or "python -m"
            "server_args": ["mcp-server-git", "--repository", "/path/to/repo"],
            "allowed_tools": ["git_status", "git_diff", "git_log", "read_file"],
        },
        # Filesystem operations
        {
            "type": "mcp",
            "server_label": "filesystem",
            "server_command": "python",
            "server_args": ["-m", "mcp_server_filesystem", "/allowed/path"],
            "allowed_tools": ["read_file", "list_directory", "search_files"],
        },
        # Time/scheduling operations
        {
            "type": "mcp",
            "server_label": "time",
            "server_command": "python",
            "server_args": ["-m", "mcp_server_time"],
            "allowed_tools": ["get_current_time", "schedule_reminder"],
        }
    ]
    
    # Real-world task combining multiple MCP servers
    plan = decompose(
        """Create a daily project status report:
        1. Check git repository for today's commits
        2. Scan project files for new TODO comments  
        3. Get current time and format report header
        4. Generate markdown report with all findings
        5. Save report to reports/daily/ directory
        """,
        tools=tools
    )
    
    results = execute(plan, run_id="daily_status_report")
    
    # Display report location
    for result in results:
        if "report" in result.output.lower() and "saved" in result.output.lower():
            print(f"Report saved: {result.output}")


# Example 6: Building Your Own MCP Server
def custom_mcp_server_info():
    """Information on creating custom MCP servers for StepChain."""
    print("\n=== Example 6: Custom MCP Server Guide ===")
    
    print("""
    Creating a custom MCP server for StepChain:
    
    1. Install MCP SDK:
       pip install mcp
    
    2. Create server script (my_mcp_server.py):
       ```python
       from mcp.server import Server
       import mcp.types as types
       
       app = Server("my-server")
       
       @app.list_tools()
       async def list_tools():
           return [
               types.Tool(
                   name="my_custom_tool",
                   description="Does something useful",
                   inputSchema={
                       "type": "object",
                       "properties": {
                           "input": {"type": "string"}
                       }
                   }
               )
           ]
       
       @app.call_tool()
       async def call_tool(name: str, arguments: dict):
           if name == "my_custom_tool":
               result = process_input(arguments["input"])
               return [types.TextContent(type="text", text=result)]
       ```
    
    3. Use in StepChain:
       ```python
       tools = [{
           "type": "mcp",
           "server_label": "my_server",
           "server_command": "python",
           "server_args": ["my_mcp_server.py"],
           "allowed_tools": ["my_custom_tool"]
       }]
       ```
    """)


if __name__ == "__main__":
    # Run examples
    basic_mcp_example()
    multi_mcp_example()
    mcp_with_custom_functions()
    
    # Async example
    asyncio.run(production_mcp_example())
    
    python_mcp_server_example()
    custom_mcp_server_info()