from ollama import Client
from app.core.settings import settings
from app.services.ollama_service import OllamaService

from app.agent.executors.tool_executor import ToolExecutor

from app.agent.runner.agent_runner import AgentRunner
from app.agent.tools.registry import ToolRegistry
from app.agent.tools.calculate_sum.definition import CALCULATE_SUM_TOOL
from app.agent.tools.get_user_name.definition import GET_USER_NAME_TOOL
from app.agent.tools.weather.definition import WEATHER_TOOL
from app.agent.tools.flaky.definition import FLAKY_TOOL
from app.agent.tools.create_task.definition import CREATE_TASK_TOOL

from app.agent.policies.retry_policy import RetryPolicy
from app.agent.policies.tool_policy import ToolPolicy
from app.agent.errors.tool_errors import (
    ToolTransientError,
    ToolTimeoutError,
    ToolValidationError,
    ToolExecutionError,
    ToolPermanentError,
)

client = Client(host=settings.OLLAMA_HOST)

policy = RetryPolicy(max_attempts=3, base_delay=0.2, max_delay=2.0)
tool_policy = ToolPolicy()
registry = ToolRegistry()
excutor = ToolExecutor(policy)

print("Before register tool")
registry.register(CREATE_TASK_TOOL)
registry.register(FLAKY_TOOL)
registry.register(CALCULATE_SUM_TOOL)
registry.register(GET_USER_NAME_TOOL)
registry.register(WEATHER_TOOL)

print("REGISTER TOOL DONE")

# arguments = {"title": "Hello World"}


# result = excutor.execute(tool, arguments)
# print("result", result)


agent_runner = AgentRunner(
    llm=OllamaService(client=client),
    tool_registry=registry,
    tool_executor=excutor,
    tool_policy=tool_policy,
)


answer = agent_runner.run("Create a task called 'Learn LangGraph'")
print("answer", answer)
# messages =>>>> [{'role': 'system', 'content': 'You are a helpful assistant. Use the weather tool when needed.'}, {'role': 'user', 'content': 'Thời tiết Huế hiện tại thế nào?'}, {'role': 'assistant', 'content': '', 'tool_calls': [ToolCall(function=Function(name='get_weather', arguments={'city': 'Huế'}))]}, {'role': 'tool', 'content': '{"city": "Hu\\u1ebf", "temperature": 20, "condition": "Sunny"}'}]
# answer nhận được: "Hiện tại ở Huế trời đang nắng với nhiệt độ là 20°C."


# answer = agent_runner.run("Hãy tính tổng 10 và 20.")
# messages =>>>> [{'role': 'system', 'content': 'You are a helpful assistant. Use the weather tool when needed.'}, {'role': 'user', 'content': 'Hãy tính tổng 10 và 20.'}, {'role': 'assistant', 'content': '', 'tool_calls': [ToolCall(function=Function(name='calculate_sum', arguments={'b': 20, 'a': 10}))]}, {'role': 'tool', 'content': '{"result": 30}'}]
# answer nhận được: "Tổng của 10 và 20 là 30."

# answer = agent_runner.run("Tên của user có id 123 là gì?")
# messages =>>>> [{'role': 'system', 'content': 'You are a helpful assistant. Use the weather tool when needed.'}, {'role': 'user', 'content': 'Tên của user có id 123 là gì?'}, {'role': 'assistant', 'content': '', 'tool_calls': [ToolCall(function=Function(name='get_user_name', arguments={'user_id': '123'}))]}, {'role': 'tool', 'content': '{"user_name": "Nhat", "123": "123"}'}]
# answer nhận được: "User with ID 123 is named Nhat."

# print(answer)
