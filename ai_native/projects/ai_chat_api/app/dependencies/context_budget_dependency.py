from app.context.context_budget import ContextBudget
from app.core.settings import settings


def get_context_budget() -> ContextBudget:
    return ContextBudget(
        context_window=settings.OLLAMA_NUM_CTX,
        reserved_output_tokens=settings.OLLAMA_NUM_PREDICT,
        safety_margin_tokens=settings.CONTEXT_SAFETY_MARGIN,
    )
