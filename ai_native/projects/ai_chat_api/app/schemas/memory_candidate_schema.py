from pydantic import BaseModel, Field
from app.schemas.memory_semantics_schema import MemorySemantics


class MemoryCandidate(BaseModel):
    content: str = Field(
        min_length=1,
    )

    semantics: MemorySemantics
