from typing_extensions import TypedDict, Annotated, Callable

from langchain_core.messages import AnyMessage, HumanMessage, AIMessage, ToolMessage

from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END

from langchain_ollama import ChatOllama

from app.core.settings import settings

llm = ChatOllama(
    model=settings.OLLAMA_MODEL,
    base_url=settings.OLLAMA_HOST,
)


class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]


@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    return f"The weather in {city} is sunny and 30°C."


@tool
def get_population(city: str) -> str:
    """Get the population of a city."""
    return f"The population of {city} is approximately 450,000."


llm_with_tools = llm.bind_tools([get_weather, get_population])


def assistant(state: State):
    response = llm_with_tools.invoke(state["messages"])

    return {"messages": [response]}


tool_node = ToolNode([get_weather, get_population])

builder = StateGraph(State)

builder.add_node("assistant", assistant)
builder.add_node("tools", tool_node)

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

result = graph.invoke(
    {"messages": [HumanMessage(content="What is the weather and population of Hue?")]}
)

print(result)
