from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    message: str


def node_a(state: State):
    print("Node a is received state input:", state)

    return {"message": f"{state['message']} -> Node A"}


def node_b(state: State):
    print("Node b is received state input:", state)

    return {"message": f"{state['message']} -> Node B"}


builder = StateGraph(State)

builder.add_node("node_a", node_a)
builder.add_node("node_b", node_b)

builder.add_edge(START, "node_a")
builder.add_edge("node_a", "node_b")
builder.add_edge("node_b", END)

graph = builder.compile()

result = graph.invoke(
    {
        "message": "Thong Nhat",
    }
)

print("Result:", result)
