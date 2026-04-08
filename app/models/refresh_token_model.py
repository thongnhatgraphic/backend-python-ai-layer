from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import UUID

class RefreshTokenModel(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: UUID = Field(foreign_key="usermodel.id")
    token: str
    is_revoked: bool = False
    expires_at: datetime