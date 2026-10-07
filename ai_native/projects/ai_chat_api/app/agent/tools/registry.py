from collections.abc import Callable
from app.agent.definitions.tool_definition import ToolDefinition


class ToolRegistry:
    def __init__(self):
        self._tools: dict[str, ToolDefinition] = {}

    def register(self, tool: ToolDefinition) -> None:
        if tool.name in self._tools:
            raise ValueError(f"Tool with name {tool.name} already registered")

        self._tools[tool.name] = tool

    def get(self, name: str) -> ToolDefinition:
        try:
            return self._tools[name]
        except KeyError:
            raise ValueError(f"Unknown tool: {name}") from None

    def get_all(self) -> list[ToolDefinition]:

        return list(self._tools.values())
