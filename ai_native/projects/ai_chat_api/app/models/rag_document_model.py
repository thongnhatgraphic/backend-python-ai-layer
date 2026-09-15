from uuid import UUID, uuid4

from pgvector.sqlalchemy import Vector
from sqlmodel import Field, SQLModel
from sqlalchemy import Column, Text


class RagDocumentModel(SQLModel, table=True):
    __tablename__ = "rag_documents"

    id: UUID = Field(primary_key=True, default_factory=uuid4)
    external_id: str = Field(nullable=False, unique=True, max_length=100)
    title: str | None = Field(
        default=None,
    )
    content: str = Field(sa_column=Column(Text, nullable=False))
    embedding: list[float] | None = Field(
        default=None,
        sa_column=Column(
            Vector(768),
            nullable=True,
        ),
    )
