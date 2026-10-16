from typing_extensions import TypedDict, Annotated

from langgraph.graph import StateGraph, START, END, message
from langgraph.types import interrupt, Command
from langgraph.prebuilt import ToolNode, tools_condition

from langchain_core.messages import AnyMessage, HumanMessage, AIMessage
from langchain_ollama import ChatOllama
from app.core.settings import settings

llm = ChatOllama(
    model=settings.OLLAMA_MODEL,
    base_url=settings.OLLAMA_HOST,
)


class State(TypedDict):
    question: str
    answer: str


def assistant(state: State) -> AnyMessage:
    response = llm.invoke([HumanMessage(content=state["question"])])

    return {"answer": response.content}


builder = StateGraph(State)

builder.add_node("assistant", assistant)

builder.add_edge(START, "assistant")
builder.add_edge("assistant", END)

graph = builder.compile()

print("=== LLM STREAMING ===")
chunk_count = 0
for message_chunk, metadata in graph.stream(
    {
        "question": (
            "Explain the difference between an AI Agent "
            "and a normal chatbot in three short sentences."
        )
    },
    stream_mode="messages",
):
    if message_chunk.content:
        chunk_count += 1
        # print(
        #     message_chunk.content,
        #     end="",
        #     flush=True,
        # )
        print(f"\nChunk {chunk_count}: " f"{message_chunk.content!r}")

        print(
            "Node:",
            metadata.get("langgraph_node"),
        )

print(f"\nTotal chunks: {chunk_count}")
