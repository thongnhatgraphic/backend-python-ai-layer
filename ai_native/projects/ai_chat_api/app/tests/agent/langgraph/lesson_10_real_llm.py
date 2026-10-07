from typing_extensions import TypedDict, Annotated, Callable

from langchain_core.messages import AnyMessage, HumanMessage, AIMessage, ToolMessage

from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
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


llm_with_tools = llm.bind_tools([get_weather])


def assistant(state: State):
    response = llm_with_tools.invoke(state["messages"])

    return {"messages": [response]}


def should_continue(state: State):
    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "tools"

    return "end"


tool_node = ToolNode([get_weather])

builder = StateGraph(State)

builder.add_node("assistant", assistant)
builder.add_node("tools", tool_node)

builder.add_edge(START, "assistant")
builder.add_conditional_edges(
    "assistant", should_continue, {"tools": "tools", "end": END}
)

builder.add_edge("tools", "assistant")

graph = builder.compile()

result = graph.invoke(
    {
        "messages": [
            HumanMessage(
                content="Please use the get_weather tool to check the weather in Hue."
            )
        ]
    }
)

print(result)
