from app.agent.tools.create_task.schema import CreateTaskInput
from app.agent.definitions.tool_definition import ToolDefinition
from app.agent.tools.create_task.tool import create_task

CREATE_TASK_TOOL = ToolDefinition(
    name="create_task",
    description="Create a task.",
    input_model=CreateTaskInput,
    function=create_task,
    require_confirmation=True,
)
