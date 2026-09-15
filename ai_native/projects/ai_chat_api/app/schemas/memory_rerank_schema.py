from pydantic import BaseModel
from app.schemas.memory_schema import Memory


class MemoryRerankResult(BaseModel):
    memory: Memory
    score: float
