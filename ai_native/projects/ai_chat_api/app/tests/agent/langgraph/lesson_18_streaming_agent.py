from typing_extensions import TypedDict, Annotated

from langgraph.graph import StateGraph, START, END, message
from langgraph.types import interrupt, Command
from langgraph.prebuilt import ToolNode, tools_condition

from langchain_core.messages import AnyMessage, HumanMessage, AIMessage, ToolMessage
from langchain_core.tools import tool

from langchain_ollama import ChatOllama
from app.core.settings import settings

llm = ChatOllama(
    model=settings.OLLAMA_MODEL,
    base_url=settings.OLLAMA_HOST,
)


@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""

    print(f"\n[TOOL EXECUTION] get_weather called for {city}")

    return f"The weather in {city} is sunny, temperature is 26°C."


llm_with_tools = llm.bind_tools([get_weather])


class State(TypedDict):
    messages: Annotated[list[AnyMessage], message.add_messages]


def assistant(state: State) -> AnyMessage:
    response = llm_with_tools.invoke(state["messages"])

    return {"messages": [response]}


builder = StateGraph(State)

tools_node = ToolNode([get_weather])

builder.add_node("assistant", assistant)
builder.add_node("tools", tools_node)

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

graph = builder.compile()

print("\n=== AGENT STREAM ===")

inputs = {
    "messages": [
        HumanMessage(
            content=(
                "Please use the get_weather tool "
                "to check the weather in Hue, "
                "then explain the result."
            )
        )
    ]
}

# graph.stream(...)
#       ↓
# Generator
#       ↓
# (mode, chunk)
#       │
#       ├── mode == "messages"
#       │       ↓
#       │   (message_chunk, metadata)
#       │
#       └── mode == "updates"
#               ↓
#           {node_name: state_update}

# for event in graph.stream(
#     inputs,
#     stream_mode=["messages", "updates"],
# ):
#     print("\n event \n", event)

# for mode, chunk in graph.stream(inputs, stream_mode=["messages", "updates"]):
#     if mode == "messages":
#         message_chunk, metadata = chunk

#         tool_call_chunks = getattr(
#             message_chunk,
#             "tool_call_chunks",
#             [],
#         )

#         if tool_call_chunks:
#             for tool_call in tool_call_chunks:
#                 name = tool_call.get("name")

#                 if name:
#                     print(f"\n[AGENT] Requesting tool: {name}")

#         if message_chunk.content:
#             print(
#                 message_chunk.content,
#                 end="",
#                 flush=True,
#             )

#     elif mode == "updates":
#         for node_name, update in chunk.items():
#             print("node_name, update", node_name)
#             print("update", update)
#             print(f"\n[GRAPH] Node completed: {node_name}")

# for mode, chunk in graph.stream(
#     inputs,
#     stream_mode=["messages", "updates"],
# ):
#     if mode == "messages":
#         message_chunk, metadata = chunk

#         # LLM yêu cầu gọi tool
#         tool_call_chunks = getattr(
#             message_chunk,
#             "tool_call_chunks",
#             [],
#         )

#         if tool_call_chunks:
#             for tool_call in tool_call_chunks:
#                 name = tool_call.get("name")

#                 if name:
#                     print(f"\n[AGENT] Requesting tool: {name}")

#         # LLM phát văn bản
#         if message_chunk.content:
#             print(
#                 message_chunk.content,
#                 end="",
#                 flush=True,
#             )

#     elif mode == "updates":
#         print("<<==========================>>")

#         for node_name, update in chunk.items():
#             print(f"\n[GRAPH UPDATE] {node_name}")

#             # Lấy những message mà node vừa cập nhật
#             for message in update.get("messages", []):
#                 if isinstance(message, ToolMessage):
#                     print(f"[TOOL RESULT] {message.content}")

# for mode, chunk in graph.stream(
#     inputs,
#     stream_mode=["messages", "updates"],
# ):
#     if mode == "messages":
#         message_chunk, metadata = chunk

#         # ToolMessage sẽ được hiển thị trong nhánh updates
#         if isinstance(message_chunk, ToolMessage):
#             continue

#         tool_call_chunks = getattr(
#             message_chunk,
#             "tool_call_chunks",
#             [],
#         )

#         if tool_call_chunks:
#             for tool_call in tool_call_chunks:
#                 name = tool_call.get("name")

#                 if name:
#                     print(f"\n[AGENT] Requesting tool: {name}")

#         if message_chunk.content:
#             print(
#                 message_chunk.content,
#                 end="",
#                 flush=True,
#             )

#     elif mode == "updates":
#         for node_name, update in chunk.items():
#             print(f"\n[GRAPH UPDATE] {node_name}")

#             for message in update.get("messages", []):
#                 if isinstance(message, ToolMessage):
#                     print(f"[TOOL RESULT] {message.content}")


# 1. mode == "messages"
# message_chunk, metadata = chunk
# chunk
#  ├── message_chunk
#  └── metadata
# message_chunk là một AIMessageChunk
# metadata: {
#     "langgraph_node": "assistant",
#     "langgraph_step": 1,
#     "ls_provider": "ollama",
#     "ls_model_name": "qwen2.5:7b",
# }


def agent_events(inputs):
    for mode, chunk in graph.stream(
        inputs,
        stream_mode=["messages", "updates"],
    ):
        if mode == "messages":
            message_chunk, metadata = chunk

            node_name = metadata.get("langgraph_node", "unknown")

            if isinstance(message_chunk, ToolMessage):
                continue

            tool_call_chunks = getattr(
                message_chunk,
                "tool_call_chunks",
                [],
            )
            if tool_call_chunks:
                for tool_call in tool_call_chunks:
                    name = tool_call.get("name")

                    if name:
                        print(f"\n[AGENT] Requesting tool: {name}")
                        yield {
                            "type": "tool_call",
                            "name": name,
                        }

            if message_chunk.content and isinstance(message_chunk.content, str):
                yield {
                    "type": "token",
                    "node": metadata.get("langgraph_node"),
                    "content": message_chunk.content,
                }

        elif mode == "updates":
            for node_name, update in chunk.items():
                # Event: node vừa có state update
                yield {
                    "type": "status",
                    "node": node_name,
                }

                # Event: tool đã trả kết quả
                for message in update.get("messages", []):
                    if isinstance(message, ToolMessage):
                        yield {
                            "type": "tool_result",
                            "name": message.name,
                            "content": message.content,
                        }


if __name__ == "__main__":
    for event in agent_events(inputs):
        print(event)
