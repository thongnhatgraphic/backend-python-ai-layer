from fastapi import Depends
from app.services.token_counter import TokenCounter

from app.dependencies.token_counter_dependency import get_token_counter
from app.context.planner_context_history_selector import PlannerContextHistorySelector
from app.core.settings import settings


def get_planner_context_history_selector(
    token_counter: TokenCounter = Depends(get_token_counter),
) -> PlannerContextHistorySelector:
    planner_context_history_selector = PlannerContextHistorySelector(
        token_counter,
        max_tokens=settings.CONTEXT_PLANNER_HISTORY_TOKENS,
    )

    return planner_context_history_selector
