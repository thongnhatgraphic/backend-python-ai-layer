from app.agent.tools.calculate_sum.schema import CalculateSumInput
from app.agent.definitions.tool_definition import ToolDefinition
from app.agent.tools.calculate_sum.tool import calculate_sum

CALCULATE_SUM_TOOL = ToolDefinition(
    name="calculate_sum",
    description="Calculate the sum of two numbers.",
    input_model=CalculateSumInput,
    function=calculate_sum,
    require_confirmation=False,
)
