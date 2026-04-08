from sqlmodel import SQLModel
from uuid import UUID
from datetime import datetime


class UserResponse(SQLModel):
    id: UUID
    username: str
    created_at: datetime

class UserLoginResponse(SQLModel):
    id: UUID
    username: str
    access_token: str
    refresh_token: str
    created_at: datetime