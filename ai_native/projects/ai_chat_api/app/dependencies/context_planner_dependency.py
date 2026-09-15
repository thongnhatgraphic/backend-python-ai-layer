from fastapi import Depends

from app.context.context_planner import ContextPlanner
from app.context.planner_context_history_selector import PlannerContextHistorySelector
from app.services.ollama_service import OllamaService
from app.dependencies.ollama_dependency import get_ollama_service
from app.dependencies.context_history_dependency import (
    get_planner_context_history_selector,
)


def get_context_planner(
    llm: OllamaService = Depends(get_ollama_service),
    history_selector: PlannerContextHistorySelector = Depends(
        get_planner_context_history_selector
    ),
) -> ContextPlanner:
    return ContextPlanner(llm=llm, history_selector=history_selector)
