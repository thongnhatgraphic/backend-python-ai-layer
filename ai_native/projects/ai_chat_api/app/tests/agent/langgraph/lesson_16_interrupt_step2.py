from typing_extensions import Annotated, TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import InMemorySaver


class State(TypedDict):
    memory_id: Annotated[str, "memory id to delete"]
    approved: bool


def request_delete(state: State):
    print(f"Requesting deletion of memory: {state['memory_id']}")

    return {}


def delete_memory(state: State):
    print(f"Deleting memory: {state['memory_id']}")

    return {}


def approval_node(state: State):
    print("approval_node: started")
    print("State current:", state)
    answer = interrupt(f"Do you approve deleting memory {state['memory_id']}?")

    print("Human answer:", answer)

    return {
        "approved": answer,
    }


def approval_router(state: State):
    if state["approved"]:
        return "approved"

    return "rejected"


builder = StateGraph(State)

builder.add_node("request_delete", request_delete)
builder.add_node("approval", approval_node)
builder.add_node("delete_memory", delete_memory)
# builder.add_node("approval_router", approval_router)

builder.add_edge(START, "request_delete")
builder.add_edge("request_delete", "approval")

builder.add_conditional_edges(
    "approval", approval_router, {"approved": "delete_memory", "rejected": END}
)


builder.add_edge("delete_memory", END)

checkpointer = InMemorySaver()

graph = builder.compile(checkpointer=checkpointer)

config = {"configurable": {"thread_id": "lesson-16-step-3"}}

result = graph.invoke(
    {
        "memory_id": "memory-123",
        "approved": False,
    },
    config=config,
)

print("First result:", result)

result = graph.invoke(
    Command(resume=True),
    config=config,
)

print("Second result:", result)
