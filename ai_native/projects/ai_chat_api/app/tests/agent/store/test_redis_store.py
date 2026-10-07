from ollama import Client
from app.core.settings import settings
from uuid import uuid4

from app.services.ollama_service import OllamaService
from app.agent.runner.agent_runner import AgentRunner
from app.agent.tools.registry import ToolRegistry
from app.agent.policies.tool_policy import ToolPolicy
from app.agent.policies.retry_policy import RetryPolicy
from app.agent.executors.tool_executor import ToolExecutor

from app.agent.tools.calculate_sum.definition import CALCULATE_SUM_TOOL
from app.agent.tools.get_user_name.definition import GET_USER_NAME_TOOL
from app.agent.tools.weather.definition import WEATHER_TOOL
from app.agent.tools.flaky.definition import FLAKY_TOOL
from app.agent.tools.create_task.definition import CREATE_TASK_TOOL

from app.agent.state import AgentState, AgentStatus, PendingConfirmation

from app.agent.confirmation.models import ConfirmationRequest
from app.agent.state_store.redis_store import RedisAgentStateStore
import redis

# client = Client(host=settings.OLLAMA_HOST)
policy = RetryPolicy(max_attempts=3, base_delay=0.2, max_delay=2.0)

client_redis = redis.Redis.from_url(
    settings.REDIS_URL,
    decode_responses=True,
)

registry = ToolRegistry()
state_store = RedisAgentStateStore(client=client_redis)

registry.register(CREATE_TASK_TOOL)
registry.register(FLAKY_TOOL)
registry.register(CALCULATE_SUM_TOOL)
registry.register(GET_USER_NAME_TOOL)
registry.register(WEATHER_TOOL)

tool_policy = ToolPolicy()
tool_executor = ToolExecutor(retry_policy=tool_policy)

agent_runner = AgentRunner(
    llm=OllamaService(client=Client(host="localhost:11434")),
    tool_registry=registry,
    tool_executor=tool_executor,
    tool_policy=tool_policy,
    state_store=state_store,
)


def test_save_agentstate():
    agent_runner.run("Create a task called 'Learn LangGraph'")


# test_save_agentstate()


def test_get_agentstate():
    state = AgentState(
        user_message="Create task",
        messages=[],
    )

    agent_runner.state_store.save(state)

    loaded = agent_runner.state_store.get(state.run_id)

    print("saved :", state)
    print("loaded:", loaded)

    print("loaded is not None", loaded is not None)
    print("loaded.run_id == state.run_id", loaded.run_id == state.run_id)
    print(" loaded.status == state.status", loaded.status == state.status)


# test_get_agentstate()


def test_pause_and_resume_with_redis():

    # Request #1
    state = agent_runner.run("Create a task called 'Learn LangGraph'")

    assert state.status == AgentStatus.WAITING_FOR_CONFIRMATION

    run_id = state.run_id

    pending = state.pending_confirmation

    print("run_id =", run_id)
    print("pending =", pending)
    loaded = state_store.get(run_id)

    print(loaded)

    # Request #2
    request = ConfirmationRequest(
        tool_call_id=pending.tool_call_id,
        approved=True,
    )

    result = agent_runner.confirm(
        run_id=run_id,
        request=request,
    )

    print("result =", result)

    print(
        "result.status == AgentStatus.COMPLETED", result.status == AgentStatus.COMPLETED
    )
    print("result.pending_confirmation is None", result.pending_confirmation is None)


test_pause_and_resume_with_redis()
