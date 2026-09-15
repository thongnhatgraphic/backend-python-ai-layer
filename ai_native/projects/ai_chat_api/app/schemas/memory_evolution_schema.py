from enum import Enum

from pydantic import BaseModel

from app.schemas.memory_schema import Memory


class MemoryEvolutionOperation(str, Enum):
    INSERT = "insert"
    UPDATE = "update"
    DUPLICATE = "duplicate"


class MemoryEvolutionResult(BaseModel):
    operation: MemoryEvolutionOperation
    memory: Memory | None = None
