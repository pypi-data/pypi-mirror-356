"""Simplified task decomposition module - 10x developer version.

Focuses on essential functionality with minimal complexity.
"""

import json
import re
from typing import Any

from stepchain.config import get_config
from stepchain.core.models import Plan, Step
from stepchain.errors import DecompositionError
from stepchain.integrations.openai import get_default_client
from stepchain.utils.logging import get_logger

logger = get_logger(__name__)


class TaskDecomposer:
    """Simple task decomposer that leverages LLM intelligence."""
    
    def __init__(self, client=None, model: str | None = None, max_steps: int = 10) -> None:
        """Initialize with minimal configuration.
        
        Args:
            client: OpenAI client (optional)
            model: Model to use (optional) 
            max_steps: Maximum steps allowed (default: 10)
        """
        self.config = get_config()
        self.client = client or get_default_client()
        self.model = model or self.config.openai_model
        self.max_steps = max_steps
    
    def decompose(self, task: str, tools: list[str | dict[str, Any]] | None = None) -> Plan:
        """Break down a task into executable steps.
        
        Args:
            task: Natural language task description
            tools: Available tools (optional)
            
        Returns:
            Plan with decomposed steps
        """
        if not task or not task.strip():
            raise DecompositionError("Task cannot be empty")
        
        # Try decomposition, retry once if needed
        for attempt in range(2):
            try:
                # Generate plan using LLM
                prompt = self._create_prompt(task, tools or [])
                response = self._call_llm(prompt)
                
                # Parse response
                plan_data = self._parse_response(response)
                
                # Create and validate plan
                plan = self._create_plan(plan_data, task, tools)
                
                # Basic validation
                self._validate_dependencies(plan)
                
                logger.info(f"Decomposed into {len(plan.steps)} steps")
                return plan
                
            except Exception as e:
                if attempt == 0:
                    logger.warning(f"First attempt failed: {e}, retrying...")
                    continue
                raise DecompositionError(f"Failed to decompose task: {e}") from e
    
    def _create_prompt(self, task: str, tools: list[str | dict[str, Any]]) -> str:
        """Create a simple, effective prompt."""
        tool_list = self._format_tools(tools)
        
        return f"""Break down this task into clear, executable steps:

TASK: {task}

TOOLS AVAILABLE: {tool_list}

Return a JSON object with this structure:
{{
    "steps": [
        {{
            "id": "step_1",
            "prompt": "Clear instruction for this step",
            "tools": ["tool1", "tool2"],  // from available tools
            "dependencies": []  // IDs of steps that must complete first
        }}
    ]
}}

Guidelines:
- Each step should do one thing well
- Use dependencies to order steps correctly  
- Maximum {self.max_steps} steps
- Keep prompts clear and actionable

Return ONLY the JSON, no other text."""
    
    def _call_llm(self, prompt: str) -> str:
        """Call LLM with the prompt."""
        response = self.client.create_completion(
            prompt=prompt,
            model=self.model,
            temperature=0.7,
            max_tokens=2000
        )
        
        content = response.get("content", "")
        if not content:
            raise DecompositionError("Empty response from LLM")
            
        return content
    
    def _parse_response(self, response: str) -> dict[str, Any]:
        """Parse LLM response with basic fallbacks."""
        try:
            # First try direct JSON parse
            data = json.loads(response)
            if self._is_valid_structure(data):
                return data
        except json.JSONDecodeError:
            pass
        
        # Try extracting JSON from code blocks
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', response, re.DOTALL)
        if json_match:
            try:
                data = json.loads(json_match.group(1))
                if self._is_valid_structure(data):
                    return data
            except json.JSONDecodeError:
                pass
        
        raise DecompositionError("Could not parse valid plan from response")
    
    def _is_valid_structure(self, data: Any) -> bool:
        """Check if data has required structure."""
        if not isinstance(data, dict) or "steps" not in data:
            return False
        
        steps = data["steps"]
        if not isinstance(steps, list) or not steps:
            return False
            
        # Each step needs at least id and prompt
        for step in steps:
            if not isinstance(step, dict):
                return False
            if not all(k in step for k in ["id", "prompt"]):
                return False
                
        return True
    
    def _create_plan(self, data: dict[str, Any], task: str, tools: list[str | dict[str, Any]] | None) -> Plan:
        """Create Plan from parsed data."""
        steps = []
        
        # Map tool names to definitions
        tool_map = self._build_tool_map(tools or [])
        
        for step_data in data["steps"]:
            # Map tools
            step_tools = step_data.get("tools", [])
            mapped_tools = self._map_tools(step_tools, tool_map)
            
            # Create step
            step = Step(
                id=step_data["id"],
                prompt=step_data["prompt"],
                tools=mapped_tools,
                dependencies=step_data.get("dependencies", [])
            )
            steps.append(step)
        
        return Plan(
            id=f"plan_{len(steps)}steps",
            goal=task,
            steps=steps
        )
    
    def _build_tool_map(self, tools: list[str | dict[str, Any]]) -> dict[str, str | dict[str, Any]]:
        """Build mapping of tool names to definitions."""
        tool_map = {}
        
        for tool in tools:
            if isinstance(tool, str):
                tool_map[tool] = tool
            elif isinstance(tool, dict):
                # Handle different tool types
                if tool.get("type") == "mcp":
                    label = tool.get("server_label", "")
                    if label:
                        tool_map[label] = tool
                    # Also map allowed tools
                    for allowed in tool.get("allowed_tools", []):
                        tool_map[allowed] = tool
                elif tool.get("type") == "function":
                    name = tool.get("function", {}).get("name")
                    if name:
                        tool_map[name] = tool
                        
        return tool_map
    
    def _map_tools(self, tool_names: list[str], tool_map: dict[str, str | dict[str, Any]]) -> list[str | dict[str, Any]]:
        """Map tool names to definitions."""
        mapped: list[str | dict[str, Any]] = []
        
        for name in tool_names:
            if name in tool_map:
                tool_def = tool_map[name]
                # Avoid duplicates
                if tool_def not in mapped:
                    mapped.append(tool_def)
            elif name in ["web_search", "code_interpreter", "file_search"]:
                # Built-in tools
                if name not in mapped:
                    mapped.append(name)
                    
        return mapped
    
    def _validate_dependencies(self, plan: Plan) -> None:
        """Validate that dependencies reference existing steps."""
        step_ids = {step.id for step in plan.steps}
        
        for step in plan.steps:
            for dep in step.dependencies:
                if dep not in step_ids:
                    raise DecompositionError(
                        f"Step '{step.id}' depends on non-existent step '{dep}'"
                    )
    
    def _format_tools(self, tools: list[str | dict[str, Any]]) -> str:
        """Format tools for prompt."""
        if not tools:
            return "web_search"
            
        names = []
        for tool in tools:
            if isinstance(tool, str):
                names.append(tool)
            elif isinstance(tool, dict):
                if tool.get("type") == "mcp":
                    label = tool.get("server_label", "mcp")
                    allowed = tool.get("allowed_tools", [])
                    if allowed:
                        names.append(f"{label}: {', '.join(allowed)}")
                    else:
                        names.append(label)
                elif tool.get("type") == "function":
                    name = tool.get("function", {}).get("name", "function")
                    names.append(name)
                    
        return ", ".join(names) if names else "web_search"


# Convenience function for simple usage
def decompose(task: str, tools: list[str | dict[str, Any]] | None = None, max_steps: int = 10) -> Plan:
    """Simple function to decompose a task.
    
    Args:
        task: Task description
        tools: Available tools (optional)
        max_steps: Maximum steps allowed
        
    Returns:
        Plan with decomposed steps
    """
    decomposer = TaskDecomposer(max_steps=max_steps)
    return decomposer.decompose(task, tools)