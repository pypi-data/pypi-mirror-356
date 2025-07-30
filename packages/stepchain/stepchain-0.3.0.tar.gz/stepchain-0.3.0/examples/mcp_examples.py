#!/usr/bin/env python3
"""MCP (Model Context Protocol) examples from OpenAI cookbook.

This demonstrates how StepChain works seamlessly with MCP tools
for connecting to external services.
"""

from stepchain import decompose, execute

def example_1_basic_mcp():
    """Basic MCP example - GitHub code search."""
    print("\n=== Example 1: Basic MCP Tool (GitHub) ===")
    
    # From OpenAI's cookbook - works out of the box
    mcp_tool = {
        "type": "mcp",
        "server_label": "gitmcp",
        "server_url": "https://gitmcp.io/openai/tiktoken",
        "allowed_tools": ["search_tiktoken_documentation", "fetch_tiktoken_documentation"],
        "require_approval": "never"
    }
    
    plan = decompose(
        "How does tiktoken work? Search the documentation for details.",
        tools=[mcp_tool]
    )
    
    print(f"Created plan with {len(plan.steps)} steps")
    for step in plan.steps:
        print(f"- {step.prompt[:60]}...")

def example_2_multi_service():
    """Connect to multiple MCP services."""
    print("\n=== Example 2: Multi-Service MCP ===")
    
    tools = [
        {
            "type": "mcp",
            "server_label": "postgres",
            "server_url": "postgresql://localhost:5432/mcp",
            "allowed_tools": ["query", "analyze_schema"],
            "require_approval": "never"
        },
        {
            "type": "mcp",
            "server_label": "slack",
            "server_url": "https://slack.com/api/mcp",
            "allowed_tools": ["send_message", "read_channel"],
            "require_approval": "never"
        },
        "web_search"  # Mix with built-in tools
    ]
    
    plan = decompose(
        "Get last week's sales from database and post summary to #sales Slack channel",
        tools=tools
    )
    
    print(f"Created plan using {len(set(str(t) for s in plan.steps for t in s.tools))} different tools")

def example_3_mcp_with_functions():
    """MCP combined with custom functions."""
    print("\n=== Example 3: MCP + Custom Functions ===")
    
    # Your custom function
    def analyze_sentiment(text: str) -> dict:
        """Analyze sentiment of text."""
        # Simplified example
        positive_words = ["good", "great", "excellent", "amazing"]
        negative_words = ["bad", "terrible", "awful", "poor"]
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        return {
            "sentiment": "positive" if positive_count > negative_count else "negative",
            "confidence": 0.8
        }
    
    tools = [
        {
            "type": "mcp",
            "server_label": "reddit",
            "server_url": "https://reddit.com/api/mcp",
            "allowed_tools": ["search_posts", "get_comments"],
            "require_approval": "never"
        },
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
            },
            "implementation": analyze_sentiment
        }
    ]
    
    plan = decompose(
        "Find recent posts about our product on Reddit and analyze sentiment",
        tools=tools
    )
    
    print(f"Plan combines MCP and custom functions across {len(plan.steps)} steps")

def example_4_financial_mcp():
    """Real-world financial analysis with MCP."""
    print("\n=== Example 4: Financial Analysis with MCP ===")
    
    tools = [
        {
            "type": "mcp",
            "server_label": "financial_data",
            "server_url": "https://api.financial.com/mcp",
            "allowed_tools": ["get_stock_data", "get_market_indices", "get_company_financials"],
            "require_approval": "never"
        },
        {
            "type": "mcp",
            "server_label": "news_api",
            "server_url": "https://newsapi.org/mcp",
            "allowed_tools": ["search_articles", "get_trending"],
            "require_approval": "never"
        },
        "code_interpreter"  # For calculations
    ]
    
    plan = decompose(
        "Analyze Apple (AAPL) stock performance, compare with NASDAQ, "
        "check recent news impact, and calculate key financial ratios",
        tools=tools
    )
    
    # Show tool usage distribution
    tool_usage = {}
    for step in plan.steps:
        for tool in step.tools:
            tool_name = tool if isinstance(tool, str) else tool.get("server_label", "unknown")
            tool_usage[tool_name] = tool_usage.get(tool_name, 0) + 1
    
    print("Tool usage in plan:")
    for tool, count in tool_usage.items():
        print(f"  - {tool}: {count} steps")

def example_5_mcp_approval_modes():
    """Different MCP approval modes."""
    print("\n=== Example 5: MCP Approval Modes ===")
    
    tools = [
        {
            "type": "mcp",
            "server_label": "production_db",
            "server_url": "postgresql://prod.example.com/mcp",
            "allowed_tools": ["read_only_query"],
            "require_approval": "never"  # Safe operations
        },
        {
            "type": "mcp",
            "server_label": "production_db_write",
            "server_url": "postgresql://prod.example.com/mcp",
            "allowed_tools": ["execute_update", "execute_delete"],
            "require_approval": "always"  # Dangerous operations
        }
    ]
    
    plan = decompose(
        "Analyze user engagement metrics and clean up old test accounts",
        tools=tools
    )
    
    print("Steps requiring approval:")
    for step in plan.steps:
        for tool in step.tools:
            if isinstance(tool, dict) and tool.get("require_approval") == "always":
                print(f"  - {step.prompt[:50]}... [REQUIRES APPROVAL]")

def main():
    """Run all MCP examples."""
    print("StepChain MCP Examples")
    print("=" * 50)
    print("Note: These examples show plan creation. Actual execution would")
    print("require valid MCP server endpoints.")
    
    example_1_basic_mcp()
    example_2_multi_service()
    example_3_mcp_with_functions()
    example_4_financial_mcp()
    example_5_mcp_approval_modes()
    
    print("\n" + "=" * 50)
    print("MCP + StepChain = External services with zero complexity")

if __name__ == "__main__":
    main()