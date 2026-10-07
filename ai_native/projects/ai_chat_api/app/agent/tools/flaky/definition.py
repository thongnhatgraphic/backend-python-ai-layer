from app.agent.definitions.tool_definition import ToolDefinition

from app.agent.tools.flaky.tool import flaky_tool

from pydantic import BaseModel


class FlakyToolInput(BaseModel):
    arg1: str


FLAKY_TOOL = ToolDefinition(
    name="flaky_tool",
    description="This Tool is used for test tool.",
    input_model=FlakyToolInput,
    function=flaky_tool,
)
