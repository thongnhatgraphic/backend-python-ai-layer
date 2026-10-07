from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    message: str


def greet(state: State):
    return {
        "message": f"Hello, {state['message']}!",
    }


builder = StateGraph(State)

builder.add_node("greet", greet)

builder.add_edge(START, "greet")
builder.add_edge("greet", END)

graph = builder.compile()

result = graph.invoke(
    {
        "message": "Thong Nhat",
    }
)

print("Result:", result)
print("builder", dir(builder))
print("builder.__getstate__()", builder.state_schema)
