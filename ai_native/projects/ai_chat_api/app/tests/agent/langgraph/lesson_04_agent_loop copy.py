from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    response_type: str
    result: str


def llm_call(state: State):
    print("LLM node input:", state)

    if state["response_type"] != "TOOL_RESULT":
        return {
            "response_type": "TOOL_CALL",
            "result": "calculate_sum(30, 70)",
        }

    return {
        "response_type": "FINAL",
        "result": "The sum is 100",
    }


def tool_node(state: State):
    print("Tool node input:", state)

    return {
        "response_type": "TOOL_RESULT",
        "result": "100",
    }


def should_continue(state: State):
    if state["response_type"] == "TOOL_CALL":
        return "tool"

    return "end"


builder = StateGraph(State)

builder.add_node("llm_call", llm_call)
builder.add_node("tool_node", tool_node)

builder.add_edge(START, "llm_call")

builder.add_conditional_edges(
    "llm_call",
    should_continue,
    {
        "tool": "tool_node",
        "end": END,
    },
)

builder.add_edge("tool_node", "llm_call")

graph = builder.compile()


result = graph.invoke(
    {
        "response_type": "",
        "result": "",
    }
)

print("Final result:", result)
