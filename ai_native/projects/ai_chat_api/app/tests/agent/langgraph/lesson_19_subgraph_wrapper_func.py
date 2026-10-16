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
    }


research_builder = StateGraph(ResearchState)

research_builder.add_node("research", research)

research_builder.add_edge(START, "research")
research_builder.add_edge("research", END)

research_graph = research_builder.compile()


class ParentState(TypedDict):
    topic: str
    answer: str


def research_workflow(state: ParentState):
    print(f"[Parent Graph] calling research subgraph... {state["topic"]}")

    # 1. Parent chọn dữ liệu đầu vào cho Child Graph
    research_result = research_graph.invoke(
        {
            "topic": state["topic"],
        }
    )
    print("research_result", research_result)
    # 2. Parent chọn dữ liệu cần lấy từ Child Graph
    draft = research_result["draft"]
    print("draft", draft)
    # 3. Chuyển đổi kết quả thành state update của Parent
    return {
        "answer": f"Summary based on: {draft}",
    }


builder = StateGraph(ParentState)

builder.add_node("research_workflow", research_workflow)

builder.add_edge(START, "research_workflow")
builder.add_edge("research_workflow", END)


graph = builder.compile()

result = graph.invoke(
    {
        "topic": "LangGraph Subgraphs",
    }
)

print("Final result:", result)
