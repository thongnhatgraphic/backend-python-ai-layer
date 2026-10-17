from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END


class ResearchState(TypedDict):
    topic: str
    draft: str
    private_state: str


def research(state: ResearchState):
    print("[Research Subgraph] researching...")

    return {
        "draft": f"Research findings about {state['topic']}",
        "private_state": "Handle logic outside of graph.",
    }


def inspect_private(state: ResearchState):
    print(
        "[Research Subgraph] private_state:",
        state["private_state"],
    )

    return {}


research_builder = StateGraph(ResearchState)

research_builder.add_node("research", research)
research_builder.add_node("inspect_private", inspect_private)

research_builder.add_edge(START, "research")
research_builder.add_edge("research", "inspect_private")
research_builder.add_edge("research", END)

research_graph = research_builder.compile()


class ParentState(TypedDict):
    topic: str
    draft: str
    answer: str


def compose_answer(state: ParentState):
    print("[Parent Graph] composing answer...")

    return {
        "answer": f"Summary based on: {state['draft']}",
        "private_state": state.get("private_state", "No private state"),
    }


builder = StateGraph(ParentState)

builder.add_node("research_graph", research_graph)

builder.add_node("compose_answer", compose_answer)

builder.add_edge(START, "research_graph")
builder.add_edge("research_graph", "compose_answer")
builder.add_edge("compose_answer", END)


graph = builder.compile()

# for chunk in graph.stream({"topic": "LangGraph Subgraphs"}, mode_stream="updates"):
#     for node_name, update in chunk.items():
#         print("node_name", node_name)
#         print("update", update)


result = graph.invoke({"topic": "LangGraph Subgraphs"})

print("Final result:", result)
print("Final result:", type(result))
