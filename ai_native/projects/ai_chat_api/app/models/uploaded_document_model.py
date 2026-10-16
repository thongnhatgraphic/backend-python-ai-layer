from uuid import UUID, uuid4
from datetime import datetime, timezone

from pgvector.sqlalchemy import Vector

from sqlmodel import Field, SQLModel
from sqlalchemy import Column, Text, UniqueConstraint


class UploadedDocumentModel(SQLModel, table=True):
    __tablename__ = "uploaded_documents"
    id: UUID = Field(primary_key=True, default_factory=uuid4)
    filename: str = Field(
        max_length=255,
        nullable=False,
    )
    content_type: str = Field(
        max_length=255,
        nullable=False,
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


class UploadedDocumentChunkModel(SQLModel, table=True):
    __tablename__ = "uploaded_document_chunks"
    __table_args__ = (
        UniqueConstraint(
            "document_id",
            "chunk_index",
            name="uq_uploaded_document_chunk_index",
        ),
    )  # Constraint bảo đảm cặp (document_id, chunk_index) là duy nhất
    id: UUID = Field(
        primary_key=True,
        default_factory=uuid4,
    )
    document_id: UUID = Field(
        foreign_key="uploaded_documents.id", nullable=False, index=True
    )
    chunk_index: int = Field(nullable=False)
    content: str = Field(sa_column=Column(Text, nullable=False))
    embedding: list[float] = Field(
        sa_column=Column(
            Vector(768),
            nullable=False,
        ),
    )


# 1. SQLModel
# Mô tả cấu trúc bảng bằng Python

# 2. Alembic revision
# Tạo migration mô tả thay đổi schema

# 3. Kiểm tra migration
# Xem Alembic dự định tạo bảng và index nào

# 4. Alembic upgrade
# Áp dụng thay đổi thực tế vào PostgreSQL
