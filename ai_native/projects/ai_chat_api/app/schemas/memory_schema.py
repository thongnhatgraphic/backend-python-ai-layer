from pydantic import BaseModel, Field
from uuid import UUID
from app.schemas.memory_candidate_schema import MemoryCandidate


class Memory(BaseModel):
    id: UUID | None = None
    content: str
    embedding: list[float] | None = None
    category: str
    memory_key: str
    cardinality: str
    temporal_behavior: str
    # embedding_model: str | None = None
    # embedded_at: datetime | None = None


class MemoryList(BaseModel):
    memories: list[MemoryCandidate]
