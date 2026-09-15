from fastapi import Depends
from app.services.context_builder import ContextBuilder
from app.services.token_counter import TokenCounter

from app.dependencies.context_budget_dependency import get_context_budget
from app.dependencies.token_counter_dependency import get_token_counter

from app.context.context_budget import ContextBudget


def get_context_builder(
    token_counter: TokenCounter = Depends(get_token_counter),
    context_budget: ContextBudget = Depends(get_context_budget),
):
    context_builder = ContextBuilder(
        token_counter=token_counter,
        context_budget=context_budget,
    )

    return context_builder
