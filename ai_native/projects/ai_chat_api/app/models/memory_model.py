from sqlmodel import SQLModel, Field
from sqlalchemy import Column, String
from uuid import UUID, uuid4
from datetime import datetime, timezone
from pgvector.sqlalchemy import Vector
from enum import Enum

# Field(...)
# là của: SQLModel

# Còn

# Column(...)
# là của: SQLAlchemy

# Nếu bạn đã tự tạo: Column(...)
# thì SQLModel sẽ không còn tự tạo Column nữa.

# Nó sẽ dùng nguyên Column bạn truyền vào.
# Tham số nullable=True nằm trong chính Column.

#                Memory
#                   │
#      ┌────────────┼────────────┐
#      ↓            ↓            ↓
#   content       semantic      embedding
#                  metadata
#                      │
#           ┌──────────┼──────────┐
#           ↓          ↓          ↓
#        category     key      behavior
#                               │
#                      ┌────────┴────────┐
#                      ↓                 ↓
#                 cardinality       temporal


class Cardinality(str, Enum):
    SINGLE = "single"
    MULTIPLE = "multiple"


class TemporalBehavior(str, Enum):
    CURRENT = "current"
    HISTORICAL = "historical"
    EVENT = "event"


# Constraint A — cardinality
# ======== single
# ======== multiple
# Constraint B — temporal_behavior
# ========current
# ========historical
# ========event
# Constraint C — Single Current Slot
# Nếu:
# cardinality = single
# AND temporal_behavior = current
# thì:
# (user_id, category, memory_key)
# phải unique.


class MemoryModel(SQLModel, table=True):
    __tablename__ = "memories"
    id: UUID = Field(primary_key=True, index=True, default_factory=uuid4)
    user_id: UUID = Field(index=True)
    content: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    embedding: list[float] | None = Field(sa_column=Column(Vector(768), nullable=True))
    category: str = Field(sa_column=Column(String(100), nullable=False))
    memory_key: str = Field(sa_column=Column(String(100), nullable=False))
    # cardinality have one of two values single or multiple
    cardinality: Cardinality = Field(
        default=Cardinality.SINGLE,
        sa_column=Column(String(20), nullable=False),
    )
    # temporal_behavior have one of three values current, historical or event
    temporal_behavior: TemporalBehavior = Field(
        default=TemporalBehavior.CURRENT,
        sa_column=Column(String(20), nullable=False),
    )


class MemorySearchResult:
    memory: MemoryModel
    score: float
