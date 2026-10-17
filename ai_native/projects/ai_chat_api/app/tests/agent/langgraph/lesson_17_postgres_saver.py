from typing_extensions import TypedDict, Annotated

from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt, Command
from langgraph.prebuilt import ToolNode, tools_condition

from langgraph.checkpoint.postgres import PostgresSaver

from app.core.settings import settings

# SQLAlchemy
#     ↓
# postgresql+psycopg://...

# Psycopg trực tiếp
#     ↓
# postgresql://...

# LangGraph PostgresSaver
#     ↓
# Psycopg trực tiếp
#     ↓
# postgresql://...

DB_URI = settings.DATABASE_URL.replace(
    "postgresql+psycopg://",
    "postgresql://",
)


class State(TypedDict):
    message: str


def hello(state: State):
    print("hello node")
    return {"message": "Hello from LangGraph"}


builder = StateGraph(State)
builder.add_node("hello", hello)

builder.add_edge(START, "hello")
builder.add_edge("hello", END)

with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
    checkpointer.setup()

    graph = builder.compile(checkpointer=checkpointer)

    config = {"configurable": {"thread_id": "lesson-17"}}

    result = graph.invoke(
        {"message": "Hello"},
        config=config,
    )

    print("Result:", result)
