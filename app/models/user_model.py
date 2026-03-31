from sqlmodel import Field, SQLModel
from datetime import datetime, timezone
from uuid import UUID, uuid4

class UserModel(SQLModel, table=True):
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True
        )
    username: str
    hashed_password: str
    created_at: datetime = Field(default_factory = lambda : datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory = lambda : datetime.now(timezone.utc))