from typing_extensions import TypedDict, Annotated

from langchain_core.messages import AnyMessage, HumanMessage, AIMessage

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages


class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]


def assistant(state: State):
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


builder = StateGraph(State)

builder.add_node("assistant", assistant)

builder.add_edge(START, "assistant")

builder.add_edge("assistant", END)

graph = builder.compile()

result = graph.invoke(
    {
        "messages": [
            HumanMessage(content="Hello! I am Nhat, What is the weather in Hue?")
        ]
    }
)


print(result)
