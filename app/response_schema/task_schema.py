from sqlmodel import SQLModel
from datetime import datetime
from uuid import UUID

class TaskResponse(SQLModel):
    id: int
    name: str
    status: str
    description: str
    progress: int
    priority: int | None 
    deadline: datetime | None
    user_id: UUID
    created_at: datetime

class TaskPaginationResponse(SQLModel): 
    tasks: list[TaskResponse] | None = None
    total: int | None = None
    page: int | None = None
    limit: int | None = None
    pages: int | None = None