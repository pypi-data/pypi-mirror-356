# Migration Guide

## Table of Contents
- [Migrating from LangChain](#migrating-from-langchain)
- [Migrating from AutoGPT](#migrating-from-autogpt)
- [Migrating from CrewAI](#migrating-from-crewai)
- [Migrating from Raw OpenAI SDK](#migrating-from-raw-openai-sdk)
- [Common Migration Patterns](#common-migration-patterns)

## Migrating from LangChain

### Key Differences
- **No Chains**: StepChain uses direct task decomposition instead of chains
- **No Agents**: The LLM itself handles planning, not agent abstractions
- **Automatic State**: Built-in persistence without memory abstractions
- **185 lines vs 50,000+**: Dramatically simpler codebase

### Before (LangChain)
```python
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain.tools import Tool
from langchain_openai import ChatOpenAI

# Complex setup
llm = ChatOpenAI(temperature=0)
memory = ConversationBufferMemory(memory_key="chat_history")

tools = [
    Tool(
        name="search",
        func=search_function,
        description="Search the web"
    ),
    Tool(
        name="calculate",
        func=calculate_function,
        description="Perform calculations"
    )
]

agent = create_openai_tools_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True,
    handle_parsing_errors=True
)

# Execute
result = agent_executor.invoke({
    "input": "Research AI trends and calculate market size"
})
```

### After (StepChain)
```python
from stepchain import decompose, execute

# Simple setup - 3 lines
plan = decompose(
    "Research AI trends and calculate market size",
    tools=["web_search", "code_interpreter"]
)
results = execute(plan, run_id="market_analysis")
```

### Migration Steps

1. **Replace Chains with Decomposition**
   ```python
   # LangChain
   chain = LLMChain(llm=llm, prompt=prompt) | OutputParser()
   
   # StepChain
   plan = decompose(task_description)
   ```

2. **Replace Agents with Direct Execution**
   ```python
   # LangChain
   agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT)
   
   # StepChain
   results = execute(plan, tools=tools)
   ```

3. **Replace Memory with Built-in State**
   ```python
   # LangChain
   memory = ConversationSummaryMemory(llm=llm)
   
   # StepChain (automatic)
   results = execute(plan, run_id="task_001", resume=True)
   ```

4. **Simplify Tool Definitions**
   ```python
   # LangChain
   @tool
   def search_tool(query: str) -> str:
       """Search the web."""
       return search_api(query)
   
   # StepChain
   tools = ["web_search"]  # Built-in
   # Or custom:
   tools = [{
       "type": "function",
       "function": {
           "name": "search",
           "description": "Search the web",
           "parameters": {"type": "object", "properties": {"query": {"type": "string"}}}
       },
       "implementation": search_api
   }]
   ```

## Migrating from AutoGPT

### Key Differences
- **No Autonomous Loops**: Deterministic execution instead of open-ended loops
- **No Plugin System**: Direct tool integration via MCP
- **Predictable Costs**: Know exactly how many steps will execute
- **Faster Execution**: No unnecessary reasoning loops

### Before (AutoGPT)
```python
# Complex configuration files
# ai_settings.yaml
ai_goals:
  - Analyze market data
  - Generate report
  - Send to stakeholders

ai_name: MarketAnalyst
ai_role: Market Research Assistant

# .env file with numerous settings
# Complex plugin setup
# Memory backend configuration
```

### After (StepChain)
```python
from stepchain import decompose, execute

plan = decompose("""
    Analyze market data
    Generate report  
    Send to stakeholders
""")
results = execute(plan)
```

### Migration Steps

1. **Convert Goals to Task Descriptions**
   ```python
   # AutoGPT: YAML configuration
   # StepChain: Natural language
   task = "Analyze market data, generate report, send to stakeholders"
   ```

2. **Replace Plugins with Tools**
   ```python
   # AutoGPT: Plugin system
   # StepChain: Direct tools
   tools = [
       "web_search",
       {"type": "mcp", "server_label": "email", ...}
   ]
   ```

3. **Remove Autonomous Loops**
   ```python
   # AutoGPT: Continuous loop until goals met
   # StepChain: Deterministic plan execution
   plan = decompose(task, max_steps=20)  # Bounded execution
   ```

## Migrating from CrewAI

### Key Differences
- **No Crew/Agent Abstractions**: LLM handles coordination
- **No Role Playing**: Direct task execution
- **Simpler Tool Integration**: No tool assignments per agent
- **Automatic Parallelization**: Based on dependencies, not crew setup

### Before (CrewAI)
```python
from crewai import Agent, Task, Crew

# Define agents with roles
researcher = Agent(
    role='Senior Research Analyst',
    goal='Find and analyze market trends',
    backstory='You are an expert at market research...',
    tools=[search_tool, scrape_tool],
    llm=llm
)

writer = Agent(
    role='Content Writer',
    goal='Write engaging market reports',
    backstory='You are a skilled technical writer...',
    tools=[writing_tool],
    llm=llm
)

# Define tasks
research_task = Task(
    description='Research AI market trends for 2024',
    agent=researcher
)

writing_task = Task(
    description='Write comprehensive market report',
    agent=writer,
    context=[research_task]
)

# Create crew
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task],
    verbose=True
)

result = crew.kickoff()
```

### After (StepChain)
```python
from stepchain import decompose, execute

# Single task description captures everything
plan = decompose("""
    Research AI market trends for 2024 and write comprehensive report:
    1. Search for latest AI market data
    2. Analyze trends and growth patterns
    3. Write executive summary
    4. Create detailed market analysis sections
    5. Format as professional report
""", tools=["web_search", "code_interpreter"])

results = execute(plan)
```

### Migration Steps

1. **Combine Agent Roles into Task Description**
   ```python
   # CrewAI: Multiple agents with roles
   # StepChain: Task description includes all requirements
   ```

2. **Flatten Task Dependencies**
   ```python
   # CrewAI: Task context and agent assignments
   # StepChain: Automatic dependency detection
   ```

3. **Unify Tool Access**
   ```python
   # CrewAI: Tools assigned per agent
   # StepChain: All tools available to all steps
   ```

## Migrating from Raw OpenAI SDK

### Key Differences
- **Automatic Retry Logic**: No manual retry implementation
- **State Persistence**: No manual checkpoint code
- **Response Parsing**: Handles malformed responses automatically
- **Tool Integration**: Simplified tool format

### Before (Raw OpenAI)
```python
import openai
import json
import time
from typing import List, Dict

def execute_with_retry(messages: List[Dict], tools: List[Dict], max_retries: 3):
    """Manual retry logic with exponential backoff."""
    for attempt in range(max_retries):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=messages,
                tools=tools,
                tool_choice="auto"
            )
            
            # Manual response parsing
            if response.choices[0].finish_reason == "tool_calls":
                tool_calls = response.choices[0].message.tool_calls
                # Manual tool execution
                for tool_call in tool_calls:
                    result = execute_tool(tool_call.function.name, 
                                        json.loads(tool_call.function.arguments))
                    # Manual result handling...
            
            return response
            
        except openai.error.RateLimitError:
            wait_time = 2 ** attempt
            time.sleep(wait_time)
        except Exception as e:
            print(f"Error: {e}")
            if attempt == max_retries - 1:
                raise

# Manual state management
def save_checkpoint(state: Dict, filepath: str):
    with open(filepath, 'w') as f:
        json.dump(state, f)

def load_checkpoint(filepath: str) -> Dict:
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
```

### After (StepChain)
```python
from stepchain import decompose, execute

# All the above functionality in 2 lines
plan = decompose("Your complex task", tools=tools)
results = execute(plan, run_id="task_001")  # Automatic retry, parsing, state
```

### Migration Steps

1. **Remove Manual Retry Logic**
   ```python
   # Before: Custom retry implementation
   # After: Built into execute()
   ```

2. **Remove State Management Code**
   ```python
   # Before: Manual checkpoint save/load
   # After: Automatic with run_id
   ```

3. **Simplify Tool Handling**
   ```python
   # Before: Manual tool execution and result processing
   # After: Automatic tool execution
   ```

## Common Migration Patterns

### Pattern 1: Complex Orchestration
```python
# Before (Any framework)
# Lots of setup code for agents, chains, memory, etc.
# Complex error handling
# Manual state management

# After (StepChain)
plan = decompose("Your complex multi-step task")
results = execute(plan, run_id="unique_id")
```

### Pattern 2: Tool Integration
```python
# Before: Complex tool wrapping
class CustomTool(BaseTool):
    name = "custom_tool"
    description = "Does something"
    
    def _run(self, query: str) -> str:
        return my_function(query)

# After: Simple dictionary
tools = [{
    "type": "function",
    "function": {
        "name": "custom_tool",
        "description": "Does something",
        "parameters": {"type": "object", "properties": {"query": {"type": "string"}}}
    },
    "implementation": my_function
}]
```

### Pattern 3: Resume Capability
```python
# Before: Manual implementation
state = load_state()
if state.get("completed_steps"):
    # Complex logic to resume from last step
    
# After: Built-in
results = execute(plan, run_id="task_001", resume=True)
```

### Pattern 4: Parallel Execution
```python
# Before: Manual thread/async management
import concurrent.futures

with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [executor.submit(process_item, item) for item in items]
    
# After: Automatic
plan = decompose("Process all items")  # StepChain detects parallelizable steps
results = execute(plan)  # Executes in parallel automatically
```

## Migration Checklist

- [ ] Identify your core task/goal
- [ ] List all tools/integrations needed
- [ ] Convert to StepChain format:
  - [ ] Write task as natural language description
  - [ ] Define tools in StepChain format
  - [ ] Replace complex setup with `decompose()`
  - [ ] Replace execution logic with `execute()`
- [ ] Add `run_id` for resume capability
- [ ] Remove unnecessary abstractions:
  - [ ] Agents/Crews
  - [ ] Chains/Pipelines  
  - [ ] Memory systems
  - [ ] Retry logic
  - [ ] State management
- [ ] Test with `resume=True` to verify state persistence

## Getting Help

If you encounter issues during migration:

1. Check the [API Reference](./api-reference.md)
2. Review [examples](../examples/)
3. Most complex frameworks features → 3 lines of StepChain
4. If genuinely stuck, you're probably overthinking it

Remember: If your migration adds code instead of removing it, you're doing it wrong.