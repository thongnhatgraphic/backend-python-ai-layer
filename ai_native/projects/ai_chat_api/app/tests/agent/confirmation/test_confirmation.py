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
from app.agent.state_store.memory_store import InMemoryAgentStateStore
from app.agent.observability.metrics import AgentMetrics
from app.agent.observability.tracing import tracer

client = Client(host=settings.OLLAMA_HOST)
policy = RetryPolicy(max_attempts=3, base_delay=0.2, max_delay=2.0)


registry = ToolRegistry()
state_store = InMemoryAgentStateStore()

registry.register(CREATE_TASK_TOOL)
registry.register(FLAKY_TOOL)
registry.register(CALCULATE_SUM_TOOL)
registry.register(GET_USER_NAME_TOOL)
registry.register(WEATHER_TOOL)

tool_policy = ToolPolicy()
retry_policy = RetryPolicy()
metrics = AgentMetrics()


class FakeLLM:
    def chat_with_tools(self, messages, tools):
        raise RuntimeError("LLM test failure")


agent_runner = AgentRunner(
    llm=OllamaService(client=Client(host="localhost:11434")),
    # llm=FakeLLM(),
    tool_registry=registry,
    tool_executor=ToolExecutor(retry_policy=retry_policy, metrics=metrics),
    tool_policy=tool_policy,
    state_store=state_store,
    metrics=metrics,
)


def test_confirm_executes_pending_tool():
    # Request 1
    state = agent_runner.run("Create a task called 'Learn LangGraph'")

    assert state.status == AgentStatus.WAITING_FOR_CONFIRMATION

    run_id = state.run_id

    stored_state = agent_runner.state_store.get(run_id)

    assert stored_state is not None
    assert stored_state.status == AgentStatus.WAITING_FOR_CONFIRMATION

    pending = stored_state.pending_confirmation

    assert pending is not None

    # Request 2
    request = ConfirmationRequest(
        tool_call_id=pending.tool_call_id,
        approved=False,
    )

    result = agent_runner.confirm(
        run_id=run_id,
        request=request,
    )

    print("result", result)

    print("agent_status:")

    for sample in list(metrics.agent_status.collect())[0].samples:
        print(
            sample.name,
            sample.labels,
            sample.value,
        )


# test_confirm_executes_pending_tool()


def test_confirm_declined():
    state = AgentState(
        step=1,
        user_message="Create task",
        messages=[],
        status=AgentStatus.WAITING_FOR_CONFIRMATION,
        pending_confirmation=PendingConfirmation(
            tool_call_id="call-123",
            tool_name="create_task",
            arguments={"title": "Learn LangGraph"},
            reason="Tool requires user confirmation before execution.",
        ),
    )

    request = ConfirmationRequest(
        tool_call_id="call-123",
        approved=True,
    )

    result = agent_runner.confirm(
        state,
        request,
    )

    print(result.status)
    print(result.pending_confirmation)


# test_confirm_declined()


def test_confirm_wrong_tool_call_id():
    state = AgentState(
        step=1,
        user_message="Create task",
        messages=[],
        status=AgentStatus.WAITING_FOR_CONFIRMATION,
        pending_confirmation=PendingConfirmation(
            tool_call_id="call-123",
            tool_name="create_task",
            arguments={"title": "Learn LangGraph"},
            reason="Tool requires user confirmation before execution.",
        ),
    )

    request = ConfirmationRequest(
        tool_call_id="call-WRONG",
        approved=True,
    )

    try:
        agent_runner.confirm(
            state,
            request,
        )
    except RuntimeError as exc:
        print("ERROR:", exc)

    print("status:", state.status)
    print("pending:", state.pending_confirmation)


# test_confirm_wrong_tool_call_id()


def test_state_store():
    store = InMemoryAgentStateStore()

    state = AgentState(
        user_message="Create task",
        messages=[],
    )

    store.save(state)

    state.status = AgentStatus.COMPLETED

    loaded = store.get(state.run_id)

    print("original:", state.status)
    print("stored:", loaded.status)


# test_state_store()


def test_logger_observability():
    agent_runner.run("Create a task called 'Learn LangGraph'")
    agent_runner.run("I want to use test tool")

    metrics = agent_runner.metrics

    print("agent_runs:")
    for sample in list(metrics.agent_runs.collect())[0].samples:
        print(sample.name, sample.value)

    print("llm_calls:")
    for sample in list(metrics.llm_calls.collect())[0].samples:
        print(sample.name, sample.value)

    print("llm_latency:")
    for sample in list(metrics.llm_latency.collect())[0].samples:
        print(sample.name, sample.labels, sample.value)

    print("tool_calls:")
    for sample in list(metrics.tool_calls.collect())[0].samples:
        print(sample.name, sample.labels, sample.value)

    print("tool_latency:")
    for sample in list(metrics.tool_latency.collect())[0].samples:
        print(sample.name, sample.labels, sample.value)

    print("agent_status:")

    for sample in list(metrics.agent_status.collect())[0].samples:
        print(
            sample.name,
            sample.labels,
            sample.value,
        )


def test_logger_observability():
    try:
        agent_runner.run("Please calculate the sum of 30 and 70")
    except Exception as exc:
        print("TEST CAUGHT:", type(exc).__name__, exc)

    metrics = agent_runner.metrics

    print("agent_runs:")
    for sample in list(metrics.agent_runs.collect())[0].samples:
        print(sample.name, sample.value)

    print("llm_calls:")
    for sample in list(metrics.llm_calls.collect())[0].samples:
        print(sample.name, sample.value)

    print("llm_latency:")
    for sample in list(metrics.llm_latency.collect())[0].samples:
        print(sample.name, sample.labels, sample.value)

    print("tool_calls:")
    for sample in list(metrics.tool_calls.collect())[0].samples:
        print(sample.name, sample.labels, sample.value)

    print("tool_latency:")
    for sample in list(metrics.tool_latency.collect())[0].samples:
        print(sample.name, sample.labels, sample.value)
    print("agent_status:")
    for sample in list(metrics.agent_status.collect())[0].samples:
        print(
            sample.name,
            sample.labels,
            sample.value,
        )


# test_logger_observability()


def test_tool_failure_trace():
    try:
        agent_runner.run("Please use the weather tool to check the weather in Hue.")
    except Exception as exc:
        print(
            "TEST CAUGHT:",
            type(exc).__name__,
            exc,
        )


test_tool_failure_trace()


def test_trace():

    with tracer.start_as_current_span("agent.run") as span:

        span.set_attribute("test", "hello")

    print("trace test completed")


# test_trace()
