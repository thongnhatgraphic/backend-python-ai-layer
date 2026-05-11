from datetime import datetime, timezone, timedelta
from sqlmodel import SQLModel, Field
from uuid import UUID

class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = ''
    status: str = 'pending'
    description: str = 'Study hard, work hard, learning is very important!!!'
    progress: int = 0  # 0 -> 100
    priority: int = 0
    deadline: datetime | None = None
    created_at: datetime = Field(default_factory= lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory= lambda: datetime.now(timezone.utc))
    user_id: UUID  | None = Field(default=None, foreign_key="usermodel.id")
