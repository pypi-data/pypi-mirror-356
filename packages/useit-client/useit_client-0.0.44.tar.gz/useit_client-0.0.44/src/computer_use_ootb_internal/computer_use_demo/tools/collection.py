"""Collection classes for managing multiple tools."""

import asyncio
from typing import Any
import inspect

from anthropic.types.beta import BetaToolUnionParam

from .base import (
    BaseAnthropicTool,
    ToolError,
    ToolFailure,
    ToolResult,
)


class ToolCollection:
    """A collection of anthropic-defined tools."""

    def __init__(self, *tools: BaseAnthropicTool):
        self._tools_by_name = {tool.name: tool for tool in tools}

    def to_params(
        self,
    ) -> list[BetaToolUnionParam]:
        return [tool.to_params() for tool in self._tools_by_name.values()]

    async def run(self, name: str, tool_input: dict[str, Any]) -> ToolResult | ToolError:
        tool = self._tools_by_name.get(name)
        if not tool:
            return ToolError(output=f"Unknown tool: {name}", action_base_type="error")

        try:
            # Check if the tool's __call__ method is a coroutine function
            if inspect.iscoroutinefunction(tool.__call__):
                return await tool(**tool_input)
            else:
                # For synchronous tools, run them in a thread to avoid blocking the event loop
                return await asyncio.to_thread(lambda: tool(**tool_input))
        except ToolError as e:
            return e
        except Exception as e:
            return ToolError(
                output=f"Tool {name} failed with exception: {e}",
                action_base_type="error",
            )
