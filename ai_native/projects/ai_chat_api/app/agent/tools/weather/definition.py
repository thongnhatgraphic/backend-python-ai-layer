from app.agent.definitions.tool_definition import ToolDefinition

from app.agent.tools.weather.schema import GetWeatherInput
from app.agent.tools.weather.tool import get_weather

WEATHER_TOOL = ToolDefinition(
    name="get_weather",
    description="Get the current weather for a city.",
    input_model=GetWeatherInput,
    function=get_weather,
)
