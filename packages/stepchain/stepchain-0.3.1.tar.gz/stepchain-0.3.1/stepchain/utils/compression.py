"""History compression strategies for managing context windows.

This module provides different strategies for compressing conversation history.
Updated to work with OpenAI Responses API input format.
"""

import logging
from abc import ABC, abstractmethod
from typing import Any

from stepchain.core.models import Step, StepResult

logger = logging.getLogger(__name__)


class CompressionStrategy(ABC):
    """Abstract base class for compression strategies."""

    @abstractmethod
    def compress(
        self,
        current_step: Step,
        previous_results: list[StepResult],
    ) -> list[dict[str, Any]]:
        """Compress history into messages for the current step (legacy)."""
        pass

    def compress_to_input(
        self,
        current_step: Step,
        previous_results: list[StepResult],
    ) -> str:
        """Compress history into a single input string for Responses API."""
        # Default implementation converts messages to input format
        messages = self.compress(current_step, previous_results)
        return self._messages_to_input(messages)

    def _messages_to_input(self, messages: list[dict[str, Any]]) -> str:
        """Convert message format to single input string."""
        parts = []
        for msg in messages:
            role = msg.get("role", "")
            content = msg.get("content", "")
            if role == "system":
                parts.append(f"[System] {content}")
            elif role == "assistant":
                parts.append(f"[Previous] {content}")
            elif role == "user":
                parts.append(content)
            else:
                parts.append(content)
        
        return "\n\n".join(parts)

    def _format_messages(
        self,
        current_step: Step,
        relevant_results: list[StepResult],
    ) -> list[dict[str, Any]]:
        """Format results into OpenAI message format (legacy)."""
        messages = []
        
        # Add previous results as context
        for result in relevant_results:
            if result.output:
                messages.append({
                    "role": "assistant",
                    "content": f"Step '{result.step_id}' result: {result.output.get('content', '')}"
                })
        
        # Add current step prompt
        messages.append({
            "role": "user",
            "content": current_step.prompt
        })
        
        return messages


class FullHistory(CompressionStrategy):
    """Keep full history without compression.

    Example:
        >>> strategy = FullHistory()
        >>> messages = strategy.compress(current_step, all_results)
        >>> input_text = strategy.compress_to_input(current_step, all_results)
    """

    def compress(
        self,
        current_step: Step,
        previous_results: list[StepResult],
    ) -> list[dict[str, Any]]:
        """Return full history without compression."""
        # Filter to only dependency results
        relevant_results = [
            r for r in previous_results
            if r.step_id in current_step.dependencies and r.output
        ]
        
        return self._format_messages(current_step, relevant_results)

    def compress_to_input(
        self,
        current_step: Step,
        previous_results: list[StepResult],
    ) -> str:
        """Format as input string for Responses API."""
        # Filter to only dependency results
        relevant_results = [
            r for r in previous_results
            if r.step_id in current_step.dependencies and r.output
        ]
        
        parts = []
        
        # Add context about previous steps if any
        if relevant_results:
            parts.append("Previous steps completed:")
            for result in relevant_results:
                if result.output and result.output.get('content'):
                    parts.append(f"- {result.step_id}: {result.output['content']}")
            parts.append("")  # Empty line
        
        # Add current step prompt
        parts.append(current_step.prompt)
        
        return "\n".join(parts)
