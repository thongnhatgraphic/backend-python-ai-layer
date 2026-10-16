from typing_extensions import TypedDict, Annotated

from langgraph.graph import StateGraph, START, END, message
from langgraph.types import interrupt, Command

from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.prebuilt import ToolNode, tools_condition


from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain_core.messages import AnyMessage, HumanMessage

from app.core.settings import settings
from pydantic import BaseModel

DB_URI = settings.DATABASE_URL.replace(
    "postgresql+psycopg://",
    "postgresql://",
)

llm = ChatOllama(
    model=settings.OLLAMA_MODEL,
    base_url=settings.OLLAMA_HOST,
)


class ApprovalDecision(BaseModel):
    approved: bool
    reason: str


@tool
def delete_memory(memory_id: str) -> str:
    """Delete a memory by its ID."""
    print("Handle logic such as validate ...")

    decision = interrupt(
        {
            "action": "delete_memory",
            "memory_id": memory_id,
            "message": f"Approve deleting memory {memory_id}?",
        },
        response_schema=ApprovalDecision,
    )

    if not decision.approved:
        print("Delete rejected.")
        return {}

    print(f"Deleting memory: {memory_id}")

    return f"Memory {memory_id} deleted successfully."


llm_with_tools = llm.bind_tools([delete_memory])


class State(TypedDict):
    messages: Annotated[list[AnyMessage], message.add_messages]


def assistant(state: State) -> str:
    response = llm_with_tools.invoke(state["messages"])

    return {"messages": [response]}


builder = StateGraph(State)

tool_node = ToolNode([delete_memory])

builder.add_node("assistant", assistant)
builder.add_node("delete_memory", delete_memory)
builder.add_node("tools", tool_node)

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


with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
    checkpointer.setup()

    graph = builder.compile(checkpointer=checkpointer)

    config = {"configurable": {"thread_id": "lesson-17-agent-hitl"}}

    result = graph.invoke(
        {
            "messages": [
                HumanMessage(content="Hello, I want to delete my memory_id = 123")
            ],
        },
        config=config,
    )

    print("Result:", result)
