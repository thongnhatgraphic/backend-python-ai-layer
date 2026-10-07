from typing_extensions import TypedDict, Annotated

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage, HumanMessage, AIMessage


class State(TypedDict):
    message: Annotated[list[AnyMessage], add_messages]


def assistant(state: State):
    return {"message": [AIMessage(content="Hello! I am your AI assistant.")]}


builder = StateGraph(State)

builder.add_node("assistant", assistant)

builder.add_edge(START, "assistant")
builder.add_edge("assistant", END)

graph = builder.compile()

result = graph.invoke(
    {
        "message": [HumanMessage(content="Hello! I am Nhat")],
    }
)

print("Result:", result)
