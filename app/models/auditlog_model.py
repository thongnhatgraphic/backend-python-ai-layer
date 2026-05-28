from sqlmodel import SQLModel, Field
from uuid import UUID
from datetime import datetime, timezone

class AuditLog(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    event_type: str
    entity_id: int
    user_id: UUID | None = Field(default=None, foreign_key="usermodel.id")

    payload: str

    created_at: datetime = Field(default_factory= lambda: datetime.now(timezone.utc))