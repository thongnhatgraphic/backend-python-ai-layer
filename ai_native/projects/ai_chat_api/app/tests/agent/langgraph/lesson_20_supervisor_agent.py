from typing_extensions import TypedDict
import json
from langgraph.graph import StateGraph, START, END
from langgraph.errors import GraphRecursionError


class SupervisorState(TypedDict):
    topic: str
    result: str
    completed_tasks: list[str]


def supervisor_router(state: SupervisorState) -> str:
    print("--------state------------", state)

    completed_tasks = state["completed_tasks"]

    if "research" not in completed_tasks:
        return "research"

    if "analysis" not in completed_tasks:
        return "analysis"

    return "finish"


def supervisor_node(state: SupervisorState) -> dict:
    print("[Supervisor]:", json.dumps(state["completed_tasks"]))

    return {}


class ResearchState(TypedDict):
    topic: str
    result: str
    completed_tasks: list[str]


def research_task(state: ResearchState):
    print("[Research Subgraph] researching...")
    # return {
    #     "result": state["result"] + f"Research findings about {state['topic']}",
    #     "completed_tasks": state["completed_tasks"] + ["research"],
    # }
    # Mô phỏng worker không báo cáo nhiệm vụ hoàn thành
    return {
        "result": state["result"],
    }


researh_builder = StateGraph(ResearchState)
researh_builder.add_node("research", research_task)

researh_builder.add_edge(START, "research")
researh_builder.add_edge("research", END)

research_graph = researh_builder.compile()


class AnalysisState(TypedDict):
    topic: str
    result: str
    completed_tasks: list[str]


def analysis_task(state: AnalysisState):
    print("[Analysis Subgraph] analyzing...")
    return {
        "result": state["result"] + f" Analysis findings about {state['topic']}",
        "completed_tasks": state["completed_tasks"] + ["analysis"],
    }


analysis_builder = StateGraph(AnalysisState)
analysis_builder.add_node("analysis", analysis_task)
analysis_builder.add_edge(START, "analysis")
analysis_builder.add_edge("analysis", END)

analysis_graph = analysis_builder.compile()


builder = StateGraph(SupervisorState)

builder.add_node("supervisor", supervisor_node)
builder.add_node("research", research_graph)
builder.add_node("analysis", analysis_graph)

builder.add_edge(START, "supervisor")
builder.add_conditional_edges(
    "supervisor",
    supervisor_router,
    {
        "research": "research",
        "analysis": "analysis",
        "finish": END,
    },
)
builder.add_edge("research", "supervisor")
builder.add_edge("analysis", "supervisor")


graph = builder.compile()


try:

    result = graph.invoke(
        {
            "topic": "AI Agent market",
            "result": "",
            "completed_tasks": [],
        },
        config={"recursion_limit": 10},
    )

    print("Final result:", result)

except GraphRecursionError as exc:
    print("Workflow stopped by recursion limit:", exc)
