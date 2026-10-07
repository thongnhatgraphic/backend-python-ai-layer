from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    message: str
    route: str


def node_a(state: State):
    print("Node A input:", state)

    return {"message": f"{state['message']} -> A", "route": "C"}


def node_b(state: State):
    print("Node B input:", state)

    return {"message": f"{state['message']} -> B"}


def node_c(state: State):
    print("Node C input:", state)

    return {"message": f"{state['message']} -> C"}


def route(state: State):
    return state["route"]


builder = StateGraph(State)

builder.add_node("node_a", node_a)
builder.add_node("node_b", node_b)
builder.add_node("node_c", node_c)

builder.add_edge(START, "node_a")

builder.add_conditional_edges(
    "node_a",
    route,
    {
        "B": "node_b",
        "C": "node_c",
    },
)

builder.add_edge("node_b", END)
builder.add_edge("node_c", END)

graph = builder.compile()


result = graph.invoke(
    {
        "message": "START",
        "route": "B",
    }
)

print(
    "The Node A is first node in graph because we did add_edge with START for 'node_a',"
    "So node would be executed first and in function invoke we define the node_b is the next node.",
    result,
)
