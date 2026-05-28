from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
from uuid import UUID


class NotificationModel(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: UUID = Field(default=None, foreign_key="usermodel.id")
    title: str | None
    message: str | None
    is_read: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
