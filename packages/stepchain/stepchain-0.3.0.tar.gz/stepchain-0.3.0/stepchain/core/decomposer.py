"""Task decomposition module for breaking complex tasks into steps.

This module uses LLMs to analyze complex tasks and generate execution plans
with support for multiple decomposition strategies, validation, and error handling.
"""

import json
import re
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any

from pydantic import ValidationError as PydanticValidationError

from stepchain.config import get_config
from stepchain.core.models import Plan, Step
from stepchain.errors import DecompositionError
from stepchain.errors import ValidationError as StepChainValidationError
from stepchain.integrations.openai import UnifiedLLMClient, get_default_client
from stepchain.utils.logging import get_logger
from stepchain.utils.retry import retry_on_exception

logger = get_logger(__name__)


class DecompositionStrategy(str, Enum):
    """Available decomposition strategies."""
    
    HIERARCHICAL = "hierarchical"  # Top-down breakdown into subtasks
    SEQUENTIAL = "sequential"      # Linear step-by-step approach
    PARALLEL = "parallel"          # Maximize parallelization
    HYBRID = "hybrid"              # Mix of sequential and parallel


# LLMClient protocol is now imported from llm_client module


class PlanValidationError(DecompositionError):
    """Raised when plan validation fails."""
    pass


class LLMError(DecompositionError):
    """Raised when LLM interaction fails."""
    def __init__(self, message: str):
        super().__init__(message, "Check your API key and network connection")


class BaseDecomposer(ABC):
    """Abstract base class for task decomposers."""
    
    @abstractmethod
    def decompose(self, task_description: str, **kwargs: Any) -> Plan:
        """Decompose a task into a plan."""
        pass


class TaskDecomposer(BaseDecomposer):
    """Decomposes complex tasks into executable steps with dependencies.
    
    This decomposer supports multiple strategies for breaking down tasks,
    validates generated plans, and provides comprehensive error handling.
    
    Attributes:
        llm_client: Client for LLM interactions
        strategy: Decomposition strategy to use
        max_steps: Maximum allowed steps in a plan
        validate_plans: Whether to validate generated plans
        
    Example:
        >>> decomposer = TaskDecomposer(strategy=DecompositionStrategy.HIERARCHICAL)
        >>> plan = decomposer.decompose(
        ...     "Create a data analysis report comparing sales trends across regions",
        ...     available_tools=["python_code", "data_visualization"]
        ... )
    """
    
    def __init__(
        self,
        llm_client: UnifiedLLMClient | None = None,
        strategy: DecompositionStrategy = DecompositionStrategy.HYBRID,
        max_steps: int | None = None,
        validate_plans: bool = True,
        model: str | None = None,
        available_tools: list[str | dict] | None = None
    ):
        """Initialize the task decomposer.
        
        Args:
            llm_client: LLM client for generating decompositions
            strategy: Decomposition strategy to use
            max_steps: Maximum allowed steps in a plan
            validate_plans: Whether to validate generated plans
            model: LLM model to use for decomposition
            
        Raises:
            ValueError: If max_steps is less than 1
        """
        self.config = get_config()
        
        if max_steps is None:
            max_steps = self.config.max_steps_per_plan
        if max_steps < 1:
            raise ValueError("max_steps must be at least 1")
            
        self.llm_client = llm_client or get_default_client()
        self.strategy = strategy
        self.max_steps = max_steps
        self.validate_plans = validate_plans
        self.model = model or self.config.openai_model
        self.available_tools = available_tools
        
        logger.info(
            f"Initialized TaskDecomposer with strategy={strategy}, "
            f"max_steps={max_steps}, validate_plans={validate_plans}"
        )
    
    # Removed - now using UnifiedLLMClient from llm_client module
    
    def decompose(
        self,
        task_description: str,
        available_tools: list[str] | None = None,
        context: dict[str, Any] | None = None,
        retry_on_validation_failure: bool = True
    ) -> Plan:
        """Decompose a complex task into a plan with steps.
        
        Args:
            task_description: Natural language description of the task
            available_tools: List of available tool names
            context: Additional context for decomposition
            retry_on_validation_failure: Whether to retry if validation fails
            
        Returns:
            Plan object with decomposed steps
            
        Raises:
            DecompositionError: If decomposition fails
            ValidationError: If plan validation fails
            LLMError: If LLM interaction fails
        """
        logger.info(f"Starting decomposition for task: {task_description[:100]}...")
        
        if not task_description or not task_description.strip():
            raise DecompositionError(
                "Task description cannot be empty",
                "Provide a clear description of what you want to accomplish"
            )
        
        if available_tools is None:
            available_tools = self.available_tools or self._get_default_tools()
            logger.debug("Using configured/default tools")
        
        context = context or {}
        attempts = 0
        max_attempts = 2 if retry_on_validation_failure else 1
        
        while attempts < max_attempts:
            attempts += 1
            
            try:
                # Create the decomposition prompt
                prompt = self._create_decomposition_prompt(
                    task_description, available_tools, context
                )
                
                # Call LLM to generate plan
                logger.debug(f"Calling LLM with strategy={self.strategy}")
                response = self._call_llm(prompt)
                
                # Parse the response into a Plan
                plan_data = self._parse_decomposition_response(response)
                
                # Create the plan
                plan = self._create_plan_from_data(
                    plan_data, task_description, available_tools
                )
                
                # Validate the plan if enabled
                if self.validate_plans:
                    self._validate_plan(plan, available_tools)
                
                logger.info(
                    f"Successfully decomposed task into {len(plan.steps)} steps"
                )
                return plan
                
            except PlanValidationError as e:
                logger.warning(
                    f"Plan validation failed (attempt {attempts}/{max_attempts}): {e}"
                )
                if attempts >= max_attempts:
                    raise
                # Add validation error to context for retry
                context["previous_validation_error"] = str(e)
                
            except Exception as e:
                logger.error(f"Decomposition failed: {e}")
                raise DecompositionError(
                    f"Failed to decompose task: {str(e)[:200]}",
                    task_description
                ) from e
        
        raise DecompositionError("Failed to generate valid plan after retries")
    
    def _get_default_tools(self) -> list[str]:
        """Get default available tools.
        
        Returns:
            List of default built-in tool names
        """
        # Return only valid built-in OpenAI tools
        return ["web_search", "code_interpreter", "file_search"]
    
    @retry_on_exception(max_retries=3)
    def _call_llm(self, prompt: str) -> str:
        """Call the LLM with error handling and retries.
        
        Args:
            prompt: The prompt to send
            
        Returns:
            LLM response text
            
        Raises:
            LLMError: If LLM call fails after retries
        """
        try:
            response = self.llm_client.create_completion(
                prompt=prompt,
                model=self.model,
                temperature=0.7,
                max_tokens=2000,
                timeout=self.config.openai_timeout,
            )
            
            if not response.get("content"):
                raise LLMError("Empty response from LLM")
                
            return response["content"]
                
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            raise LLMError(f"Failed to call LLM: {e}") from e
    
    def _create_decomposition_prompt(
        self, task: str, tools: list[str], context: dict[str, Any]
    ) -> str:
        """Create the prompt for task decomposition based on strategy.
        
        Args:
            task: Task description
            tools: Available tools
            context: Additional context
            
        Returns:
            Formatted prompt string
        """
        base_prompt = (
            f"""You are a task decomposition expert. Break down the following complex task """
            f"""into discrete, executable steps.

TASK: {task}

AVAILABLE TOOLS: {self._format_tools_for_prompt(tools)}

Please decompose this task into a JSON structure with the following format:
{{
    "steps": [
        {{
            "id": "step_1",
            "prompt": "Clear instruction for what to do",
            "tools": ["tool1", "tool2"],
            "dependencies": [],
            "rationale": "Why this step is needed",
            "expected_output": "What this step should produce"
        }},
        {{
            "id": "step_2", 
            "prompt": "Next instruction",
            "tools": ["tool3"],
            "dependencies": ["step_1"],
            "rationale": "Why this step is needed",
            "expected_output": "What this step should produce"
        }}
    ]
}}

DECOMPOSITION STRATEGY: {self.strategy.value}

{self._get_strategy_instructions()}

Requirements:
1. Each step should be atomic and focused on a single objective
2. Use descriptive step IDs that indicate the purpose
3. Specify dependencies to ensure correct execution order
4. Select appropriate tools for each step
5. Provide clear, actionable prompts
6. Consider data flow between steps
7. Maximum {self.max_steps} steps allowed
8. Ensure all dependencies reference existing steps
9. Tools must be from the available list

{self._get_context_section(context)}

Respond with ONLY the JSON structure, no additional text."""
        )
        
        return base_prompt
    
    def _get_strategy_instructions(self) -> str:
        """Get strategy-specific instructions.
        
        Returns:
            Instructions for the selected strategy
        """
        instructions = {
            DecompositionStrategy.HIERARCHICAL: (
                "Use a hierarchical approach: break the task into major phases, "
                "then break each phase into specific steps. Focus on logical grouping."
            ),
            DecompositionStrategy.SEQUENTIAL: (
                "Use a sequential approach: create a linear chain of steps where "
                "each step depends on the previous one. Minimize parallelization."
            ),
            DecompositionStrategy.PARALLEL: (
                "Use a parallel approach: maximize concurrent execution by minimizing "
                "dependencies. Group independent tasks to run simultaneously."
            ),
            DecompositionStrategy.HYBRID: (
                "Use a hybrid approach: balance sequential flow with parallel execution. "
                "Identify natural parallelization opportunities while maintaining logical order."
            )
        }
        return instructions.get(self.strategy, "")
    
    def _get_context_section(self, context: dict[str, Any]) -> str:
        """Format additional context for the prompt.
        
        Args:
            context: Context dictionary
            
        Returns:
            Formatted context section
        """
        if not context:
            return ""
            
        sections = ["\nADDITIONAL CONTEXT:"]
        
        if "previous_validation_error" in context:
            sections.append(
                f"Previous attempt failed validation: {context['previous_validation_error']}"
            )
            
        if "constraints" in context:
            sections.append(f"Constraints: {context['constraints']}")
            
        if "preferences" in context:
            sections.append(f"Preferences: {context['preferences']}")
            
        return "\n".join(sections)
    
    def _parse_decomposition_response(self, response: str) -> dict[str, Any]:
        """Parse the LLM response into plan data.
        
        Args:
            response: Raw LLM response
            
        Returns:
            Parsed plan data dictionary
            
        Raises:
            DecompositionError: If parsing fails completely
        """
        logger.debug("Parsing LLM response")
        
        try:
            # Try to extract JSON from response
            json_patterns = [
                r'\{[^{}]*\{[^{}]*\}[^{}]*\}',  # Nested JSON
                r'\{.*\}',  # Simple JSON
                r'```json\s*(.*)\s*```',  # JSON in code blocks
                r'```\s*(.*)\s*```'  # Generic code blocks
            ]
            
            for pattern in json_patterns:
                matches = re.findall(pattern, response, re.DOTALL)
                for match in matches:
                    try:
                        # Clean up the match
                        if isinstance(match, tuple):
                            match = match[0]
                        cleaned = match.strip()
                        
                        # Try to parse
                        data = json.loads(cleaned)
                        if self._is_valid_plan_structure(data):
                            logger.debug("Successfully parsed plan data")
                            return data
                    except json.JSONDecodeError:
                        continue
            
            # If no valid JSON found, try to parse the entire response
            data = json.loads(response)
            if self._is_valid_plan_structure(data):
                return data
                
        except Exception as e:
            logger.error(f"Failed to parse response: {e}")
            
        # If all parsing fails, raise error with helpful hint
        raise DecompositionError(
            "Failed to parse LLM response into valid plan structure",
            "The LLM did not return valid JSON. Try simplifying your task or check API status"
        )
    
    def _is_valid_plan_structure(self, data: Any) -> bool:
        """Check if data has valid plan structure.
        
        Args:
            data: Data to check
            
        Returns:
            True if valid structure, False otherwise
        """
        if not isinstance(data, dict):
            return False
            
        if "steps" not in data or not isinstance(data["steps"], list):
            return False
            
        if not data["steps"]:
            return False
            
        # Check each step has minimum required fields
        for step in data["steps"]:
            if not isinstance(step, dict):
                return False
            if not all(key in step for key in ["id", "prompt"]):
                return False
                
        return True
    
    def _create_plan_from_data(
        self,
        plan_data: dict[str, Any],
        task_description: str,
        available_tools: list[str]
    ) -> Plan:
        """Create a Plan object from parsed data.
        
        Args:
            plan_data: Parsed plan data
            task_description: Original task description
            available_tools: Available tools
            
        Returns:
            Plan object
            
        Raises:
            ValidationError: If step creation fails
        """
        logger.debug(f"Creating plan with {len(plan_data['steps'])} steps")
        
        steps = []
        for i, step_data in enumerate(plan_data["steps"]):
            try:
                # Process tools - map tool names to actual tool objects
                step_tools = step_data.get("tools", [])
                if isinstance(step_tools, str):
                    step_tools = [step_tools]
                
                # Map tool names to actual tool definitions
                mapped_tools = self._map_tools_to_definitions(step_tools, available_tools)
                
                # Create step with validation
                step = Step(
                    id=step_data["id"],
                    prompt=step_data["prompt"],
                    tools=mapped_tools,
                    dependencies=step_data.get("dependencies", []),
                    metadata={
                        "rationale": step_data.get("rationale", ""),
                        "expected_output": step_data.get("expected_output", ""),
                        "step_index": i,
                        "strategy": self.strategy.value
                    }
                )
                steps.append(step)
                
            except (PydanticValidationError, KeyError) as e:
                logger.error(f"Failed to create step {i}: {e}")
                raise StepChainValidationError(
                    f"Invalid step data at index {i}: {e}",
                    field=f"steps[{i}]"
                ) from e
        
        # Create plan with metadata
        plan_id = self._generate_plan_id(task_description)
        
        return Plan(
            id=plan_id,
            goal=task_description,
            steps=steps,
            metadata={
                "original_task": task_description,
                "decomposition_strategy": self.strategy.value,
                "available_tools": available_tools,
                "total_steps": len(steps),
                "max_parallel_steps": self._calculate_max_parallel_steps(steps)
            }
        )
    
    def _generate_plan_id(self, task_description: str) -> str:
        """Generate a unique plan ID.
        
        Args:
            task_description: Task description
            
        Returns:
            Plan ID
        """
        import hashlib
        from datetime import UTC, datetime
        
        # Create a hash of the task for uniqueness
        task_hash = hashlib.md5(task_description.encode()).hexdigest()[:8]
        timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
        
        return f"plan_{self.strategy.value}_{task_hash}_{timestamp}"
    
    def _calculate_max_parallel_steps(self, steps: list[Step]) -> int:
        """Calculate maximum number of steps that can run in parallel.
        
        Args:
            steps: List of steps
            
        Returns:
            Maximum parallel steps
        """
        if not steps:
            return 0
            
        # Group steps by dependency depth
        depth_groups: dict[int, list[Step]] = {}
        for step in steps:
            depth = self._get_dependency_depth(step, steps)
            if depth not in depth_groups:
                depth_groups[depth] = []
            depth_groups[depth].append(step)
        
        # Maximum parallel is the largest group size
        return max(len(group) for group in depth_groups.values())
    
    def _get_dependency_depth(self, step: Step, all_steps: list[Step]) -> int:
        """Get the dependency depth of a step.
        
        Args:
            step: Step to check
            all_steps: All steps in the plan
            
        Returns:
            Dependency depth (0 for no dependencies)
        """
        if not step.dependencies:
            return 0
            
        step_map = {s.id: s for s in all_steps}
        max_depth = 0
        
        for dep_id in step.dependencies:
            if dep_id in step_map:
                dep_step = step_map[dep_id]
                depth = 1 + self._get_dependency_depth(dep_step, all_steps)
                max_depth = max(max_depth, depth)
                
        return max_depth
    
    def _validate_plan(self, plan: Plan, available_tools: list[str]) -> None:
        """Validate a generated plan.
        
        Args:
            plan: Plan to validate
            available_tools: Available tools
            
        Raises:
            ValidationError: If validation fails
        """
        logger.debug("Validating generated plan")
        
        # Check step count
        if len(plan.steps) > self.max_steps:
            raise PlanValidationError(
                f"Plan has {len(plan.steps)} steps, exceeding maximum of {self.max_steps}"
            )
        
        if not plan.steps:
            raise PlanValidationError("Plan has no steps")
        
        # Validate dependencies
        try:
            plan.validate_dependencies()
        except ValueError as e:
            raise PlanValidationError(f"Dependency validation failed: {e}") from e
        
        # Check for circular dependencies
        if self._has_circular_dependencies(plan.steps):
            raise PlanValidationError("Plan contains circular dependencies")
        
        # Validate tools - check both strings and dicts
        available_tool_names = self._get_tool_names(available_tools)
        for step in plan.steps:
            for tool in step.tools:
                if isinstance(tool, str):
                    if tool not in available_tool_names:
                        raise PlanValidationError(
                            f"Step '{step.id}' uses unavailable tool '{tool}'"
                        )
                elif isinstance(tool, dict):
                    # For dicts, validate they have required fields
                    if "type" not in tool:
                        raise PlanValidationError(
                            f"Step '{step.id}' has tool without 'type' field"
                        )
                else:
                    raise PlanValidationError(
                        f"Step '{step.id}' has invalid tool format: {type(tool)}"
                    )
        
        # Validate step IDs are unique
        step_ids = [step.id for step in plan.steps]
        if len(step_ids) != len(set(step_ids)):
            raise PlanValidationError("Plan contains duplicate step IDs")
        
        # Validate prompts are not empty
        for step in plan.steps:
            if not step.prompt or not step.prompt.strip():
                raise PlanValidationError(f"Step '{step.id}' has empty prompt")
        
        logger.info("Plan validation passed")
    
    def _has_circular_dependencies(self, steps: list[Step]) -> bool:
        """Check if steps have circular dependencies.
        
        Args:
            steps: List of steps to check
            
        Returns:
            True if circular dependencies exist
        """
        step_map = {step.id: step for step in steps}
        
        def has_cycle(step_id: str, visited: set[str], stack: set[str]) -> bool:
            visited.add(step_id)
            stack.add(step_id)
            
            step = step_map.get(step_id)
            if step:
                for dep_id in step.dependencies:
                    if dep_id in stack or (
                        dep_id not in visited and has_cycle(dep_id, visited, stack)
                    ):
                        return True
            
            stack.remove(step_id)
            return False
        
        visited: set[str] = set()
        return any(
            step.id not in visited and has_cycle(step.id, visited, set())
            for step in steps
        )
    
    def _format_tools_for_prompt(self, tools: list[str | dict]) -> str:
        """Format tools list for the decomposition prompt.
        
        Args:
            tools: List of tool specifications
            
        Returns:
            Human-readable string of available tools
        """
        tool_descriptions = []
        for tool in tools:
            if isinstance(tool, str):
                tool_descriptions.append(tool)
            elif isinstance(tool, dict):
                if tool.get("type") == "mcp":
                    label = tool.get("server_label", "mcp_server")
                    allowed = tool.get("allowed_tools", [])
                    if allowed:
                        tool_descriptions.append(f"{label} ({', '.join(allowed)})")
                    else:
                        tool_descriptions.append(label)
                elif tool.get("type") == "function":
                    name = tool.get("function", {}).get("name", "custom_function")
                    tool_descriptions.append(name)
                else:
                    tool_descriptions.append(f"custom_tool_{tool.get('type', 'unknown')}")
        
        return ", ".join(tool_descriptions)
    
    def _get_tool_names(self, tools: list[str | dict]) -> set[str]:
        """Extract all tool names from mixed tool list.
        
        Args:
            tools: List of tool specifications
            
        Returns:
            Set of all available tool names
        """
        names = set()
        for tool in tools:
            if isinstance(tool, str):
                names.add(tool)
            elif isinstance(tool, dict):
                if tool.get("type") == "mcp":
                    # Add the server label itself
                    label = tool.get("server_label", "")
                    if label:
                        names.add(label)
                    # Add all allowed tools from MCP server
                    allowed = tool.get("allowed_tools", [])
                    names.update(allowed)
                elif tool.get("type") == "function":
                    # Add function name
                    name = tool.get("function", {}).get("name")
                    if name:
                        names.add(name)
        
        return names
    
    def _map_tools_to_definitions(
        self, tool_names: list[str], available_tools: list[str | dict[str, Any]]
    ) -> list[str | dict[str, Any]]:
        """Map tool names from LLM response to actual tool definitions.
        
        Args:
            tool_names: Tool names from LLM response (may include MCP prefixes)
            available_tools: Available tool definitions
            
        Returns:
            List of mapped tool definitions
        """
        mapped = []
        
        # Create a mapping of tool names to definitions
        tool_map = {}
        for tool in available_tools:
            if isinstance(tool, str):
                tool_map[tool] = tool
            elif isinstance(tool, dict):
                if tool.get("type") == "mcp":
                    # Map MCP server by its label
                    label = tool.get("server_label", "")
                    if label:
                        tool_map[label] = tool
                    # Also map individual allowed tools
                    for allowed in tool.get("allowed_tools", []):
                        # Map both "tool_name" and "server_label.tool_name"
                        tool_map[allowed] = tool
                        tool_map[f"{label}.{allowed}"] = tool
                elif tool.get("type") == "function":
                    name = tool.get("function", {}).get("name")
                    if name:
                        tool_map[name] = tool
        
        # Map each requested tool
        for name in tool_names:
            if name in tool_map:
                # Found exact match
                tool_def = tool_map[name]
                # Avoid duplicates
                if tool_def not in mapped:
                    mapped.append(tool_def)
            else:
                # Try to find partial match (e.g., "search_code" in "github_tools.search_code")
                found = False
                for key, tool_def in tool_map.items():
                    if name.endswith(f".{key}") or key == name:
                        if tool_def not in mapped:
                            mapped.append(tool_def)
                        found = True
                        break
                
                if not found:
                    # If not found in map, check if it's a valid built-in tool
                    if name in ["web_search", "code_interpreter", "file_search"]:
                        logger.debug(f"Using built-in tool '{name}'")
                        mapped.append(name)
                    else:
                        logger.warning(f"Tool '{name}' not found in available tools, skipping")
        
        return mapped


# TemplateBasedDecomposer removed for MVP simplicity - use TaskDecomposer instead


# DecomposerFactory removed for MVP simplicity - use TaskDecomposer directly