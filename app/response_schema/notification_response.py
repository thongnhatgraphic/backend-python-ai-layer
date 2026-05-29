from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
class NotificationResponse(BaseModel):
    id: int
    user_id: UUID
    title: str
    message: str
    is_read: bool
    created_at: datetime

class NotificationListResponse(BaseModel):
    data: list[NotificationResponse]