from typing_extensions import Annotated, TypedDict

from langgraph.graph import StateGraph, START, END, message

from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import ToolNode, tools_condition


from langchain_core.messages import AnyMessage, HumanMessage, AIMessage, ToolMessage
from langchain_core.tools import tool
from langchain_ollama import ChatOllama

from uuid import uuid4
from app.core.settings import settings

# from langgraph.graph.message import add_messages

llm = ChatOllama(
    model=settings.OLLAMA_MODEL,
    base_url=settings.OLLAMA_HOST,
)
#   ┌──────────────┐
#   │     LLM      │
#   └──────┬───────┘
#          │
#     tool call?
#      /       \
#    no         yes
#    ↓           ↓
#   END        ToolNode
#                │
#                ▼
#         delete_memory()
#                │
#            interrupt()
#                │
#                ⏸
#                │
#         Command(resume)
#                │
#                ▼
#           ToolMessage
#                │
#                ▼
#               LLM


@tool
def delete_memory(memory_id: str) -> str:
    """Delete a memory by its ID."""

    print(f"\nBefore deleting memory: {memory_id}")

    decision = interrupt(
        {
            "action": "delete_memory",
            "memory_id": memory_id,
            "message": f"Approve deleting memory {memory_id}?",
        }
    )

    print("Human decision:", decision)

    if not decision["approved"]:
        reason = decision.get("reason", "No reason provided")

        return (
            f"Deletion of memory {memory_id} was rejected by the user. "
            f"Reason: {reason}"
        )

    print(f"Deleting memory: {memory_id}")

    return f"Memory {memory_id} deleted successfully."


llm_with_tools = llm.bind_tools([delete_memory])


class State(TypedDict):
    messages: Annotated[list[AnyMessage], message.add_messages]
    # memory_id: Annotated[str, "memory id to delete"]
    # approved: bool


def assistant(state: State):
    response = llm_with_tools.invoke(state["messages"])
    print("\n response \n", response)
    return {"messages": [response]}


tool_node = ToolNode([delete_memory])

builder = StateGraph(State)

builder.add_node("tools", tool_node)
builder.add_node("assistant", assistant)


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

checkpointer = InMemorySaver()

graph = builder.compile(checkpointer=checkpointer)

config = {"configurable": {"thread_id": str(uuid4())}}


memory_id_random = str(uuid4())


result = graph.invoke(
    {
        "messages": [
            HumanMessage(
                content=f"Hello! I am Nhat, I want to use the delete_memory tool to delete a memory id={memory_id_random}"
            )
        ]
    },
    config=config,
)

print("First result:", result)

print("\n ================================================ \n")
result = graph.invoke(
    Command(
        resume={
            "approved": True,
            "reason": "I explicitly confirmed the deletion.",
        }
    ),
    config=config,
)

print("Second result:", result)
