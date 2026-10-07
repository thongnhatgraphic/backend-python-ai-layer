from app.agent.definitions.tool_definition import ToolDefinition
from app.agent.tools.get_user_name.schema import GetUserNameInput
from app.agent.tools.get_user_name.tool import get_user_name

GET_USER_NAME_TOOL = ToolDefinition(
    name="get_user_name",
    description="Get the name of a user.",
    input_model=GetUserNameInput,
    function=get_user_name,
)
