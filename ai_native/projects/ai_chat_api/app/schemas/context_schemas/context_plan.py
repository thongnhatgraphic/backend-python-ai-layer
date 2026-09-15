from pydantic import BaseModel
from app.context.context_priority import ContextImportance


class ContextSourcePlan(BaseModel):
    importance: ContextImportance


class ContextPlan(BaseModel):
    memory: ContextSourcePlan
    rag: ContextSourcePlan
    history: ContextSourcePlan
