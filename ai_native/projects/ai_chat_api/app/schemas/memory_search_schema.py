from pydantic import BaseModel
from app.schemas.memory_schema import Memory


class MemorySearchResult(BaseModel):
    memory: Memory
    score: float
