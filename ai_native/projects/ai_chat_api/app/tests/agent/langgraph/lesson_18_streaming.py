from typing_extensions import TypedDict, Annotated

from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt, Command
from langgraph.prebuilt import ToolNode, tools_condition


class State(TypedDict):
    topic: str
    draft: str
    answer: str


def prepare(state: State):
    print("prepare node: running")

    return {"draft": f"Prepared topic: {state['topic']}"}


def compose(state: State):
    print("compose node: running")

    return {"answer": f"Final answer based on: {state['draft']}"}


builder = StateGraph(State)

builder.add_node("prepare", prepare)
builder.add_node("compose", compose)


builder.add_edge(START, "prepare")
builder.add_edge("prepare", "compose")
builder.add_edge("compose", END)

graph = builder.compile()


initial_input = {"topic": "LangGraph Streaming"}

# print("\n=== INVOKE ===")

# result = graph.invoke(initial_input)

# print("Final result:", result)

# print("\n=== STREAM UPDATES ===")


# for chunk in graph.stream(
#     initial_input,
#     stream_mode="updates",
# ):
#     print(chunk)

print("\n=== STREAM UPDATES ===")


for chunk in graph.stream(
    initial_input,
    stream_mode="messages",
):
    print(chunk)
