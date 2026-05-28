from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
from uuid import UUID


class AnalyticModel(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: UUID | None = Field(default=None, foreign_key="usermodel.id", unique=True)
    total_tasks_created: int = 0
    updated_at: datetime = Field(default_factory= lambda: datetime.now(timezone.utc))