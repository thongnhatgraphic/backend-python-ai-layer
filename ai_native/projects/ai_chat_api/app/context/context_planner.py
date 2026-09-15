# ContextPlanner
#        │
#        │ importance
#        ▼
# ContextCandidate
#        │
#        │ importance + demand
#        ▼
# ContextAllocator
#        │
#        │ global budget
#        ▼
# ContextAllocation
#        │
#        ├── memory_tokens
#        ├── rag_tokens
#        └── history_tokens
#        │
#        ▼
# ContextBuilder

from app.prompts.context_planner_system_prompt import (
    build_context_planner_system_prompt,
)
from app.prompts.context_planner_user_prompt import build_context_planner_user_prompt
from app.schemas.context_schemas.context_plan import ContextPlan
from app.services.ollama_service import OllamaService
from app.context.planner_context_history_selector import PlannerContextHistorySelector


class ContextPlanner:
    def __init__(
        self, llm: OllamaService, history_selector: PlannerContextHistorySelector
    ):
        self.llm = llm
        self.history_selector = history_selector

    def plan(self, user_message: str, history: list[dict[str, str]]) -> ContextPlan:

        planner_history = self.history_selector.select(history)

        system_prompt = build_context_planner_system_prompt()

        user_prompt = build_context_planner_user_prompt(
            user_message=user_message,
            history=planner_history,
        )

        messages = [
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ]

        return self.llm.generate_structured(
            messages=messages,
            response_model=ContextPlan,
        )
