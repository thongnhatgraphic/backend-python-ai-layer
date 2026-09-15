from pydantic import BaseModel
from app.context.context_priority import ContextImportance


class ContextCandidate(BaseModel):
    name: str
    demand_tokens: int
    max_tokens: int
    priority: ContextImportance


# Memory HIGH = 500         2
# RAG HIGH = 6000           2
# History MEDIUM = 1000     1

# Budget = 5000

# total_weight = 5

# 5000 2 / 5 => 2000
