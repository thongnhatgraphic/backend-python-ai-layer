from sqlmodel import SQLModel, Field, Column
from uuid import UUID, uuid4
from datetime import datetime, timezone
from pgvector.sqlalchemy import Vector


class MemoryModel(SQLModel, table=True):
    __tablename__ = "memories"
    id: UUID = Field(primary_key=True, index=True, default_factory=uuid4)
    user_id: UUID = Field(index=True)
    content: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    embedding: list[float] = Field(sa_column=Column(Vector(768)), nullable=True)


class MemorySearchResult:
    memory: MemoryModel
    score: float
