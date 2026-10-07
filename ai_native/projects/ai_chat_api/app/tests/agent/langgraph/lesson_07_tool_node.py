from typing_extensions import TypedDict, Annotated

from langchain_core.messages import AnyMessage, HumanMessage, AIMessage, ToolMessage

from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langgraph.graph.message import add_messages

from langchain_core.tools import tool


class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]


@tool
def get_weather(city: str) -> str:
    """Get the weather for a city."""
    return f"The weather in {city} is sunny and 30°C"


def assistant(state: State):
    last_message = state["messages"][-1]
    if type(last_message) == ToolMessage:
        return {
            "messages": [
                AIMessage(
                    content=last_message.content,
                ),
            ]
        }

    return {
        "messages": [
            AIMessage(
                content="",
                tool_calls=[
                    {
                        "name": "get_weather",
                        "args": {"city": "Hue"},
                        "id": "call_1",
                        "type": "tool_call",
                    }
                ],
            ),
        ]
    }


def should_continue(state: State):
    last_message = state["messages"][-1]

    print("\n Should continue? \n")

    if last_message.tool_calls:
        return "tools"

    return "end"


tool_node = ToolNode([get_weather])

builder = StateGraph(State)


builder.add_node("assistant", assistant)
builder.add_node("tools", tool_node)

builder.add_edge(START, "assistant")

builder.add_conditional_edges(
    "assistant",
    should_continue,
    {
        "tools": "tools",
        "end": END,
    },
)

builder.add_edge("tools", "assistant")


graph = builder.compile()

result = graph.invoke(
    {
        "messages": [
            HumanMessage(content="Hello! I am Nhat, What is the weather in Hue?")
        ]
    }
)


print(result)
