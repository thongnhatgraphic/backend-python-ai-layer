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

