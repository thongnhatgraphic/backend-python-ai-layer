from typing_extensions import TypedDict, Annotated

from langchain_core.messages import AnyMessage, HumanMessage, AIMessage, ToolMessage

from langchain_core.tools import tool
from langgraph.types import RetryPolicy
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition

from langchain_ollama import ChatOllama

from app.core.settings import settings
from app.agent.errors.tool_errors import ToolError

llm = ChatOllama(
    model=settings.OLLAMA_MODEL,
    base_url=settings.OLLAMA_HOST,
)


class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]


# Tool failure
# ├── immediate exception
# ├── timeout
# ├── validation error
# └── transient failure

attempts = 0


@tool
def flaky_tool() -> str:
    """A tool that fails twice and then succeeds."""
    global attempts

    attempts += 1

    print(f"flaky_tool attempt = {attempts}")

    if attempts < 3:
        raise RuntimeError("Temporary failure")

    return "Tool succeeded!"


@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    return f"The weather in {city} is sunny and 30°C."


@tool
def get_population(city: str) -> str:
    """Get the population of a city."""
    return f"The population of {city} is approximately 450,000."
    # raise RuntimeError("Population service is unavailable.")


llm_with_tools = llm.bind_tools([get_weather, get_population, flaky_tool])


def handle_tool_error(error: Exception) -> str:
    return "The population service is temporarily unavailable."


def assistant(state: State):
    response = llm_with_tools.invoke(state["messages"])

    return {"messages": [response]}


tool_node = ToolNode(
    [get_weather, get_population, flaky_tool],
    handle_tool_errors=False,
)

builder = StateGraph(State)

builder.add_node("assistant", assistant)


builder.add_node(
    "tools",
    tool_node,
    retry_policy=RetryPolicy(
        max_attempts=3,
        retry_on=RuntimeError,
    ),
)
builder.add_edge(START, "assistant")
builder.add_conditional_edges(
    "assistant",
    tools_condition,
    {
        "tools": "tools",
        "__end__": END,
    },
)

builder.add_edge("tools", "assistant")

graph = builder.compile()


result = graph.invoke({"messages": [HumanMessage(content="I want to use flaky_tool")]})

print(result)
