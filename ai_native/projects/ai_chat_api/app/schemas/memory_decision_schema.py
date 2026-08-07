from enum import Enum
from pydantic import BaseModel


class MemoryAction(str, Enum):
    INSERT = "insert"
    DUPLICATE = "duplicate"
    MERGE = "merge"
    UPDATE = "update"


class MemoryDecision(BaseModel):
    action: MemoryAction
    candidate_index: int | None = None
    reason: str
