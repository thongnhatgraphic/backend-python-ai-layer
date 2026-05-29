from fastapi import APIRouter, Depends
from pydantic import BaseModel
from uuid import UUID
from sqlmodel import Session

from app.response_schema.notification_response import NotificationListResponse
from app.repositories.notification_repository import NotificationRepository
from app.services.notification_service import NotificationService
from app.database import get_session
from app.dependencies.auth_dependency import get_current_user

router = APIRouter()

def get_notification_service(
        session: Session = Depends(get_session),
    ):
    repository = NotificationRepository(session=session)
    return NotificationService(repository)


@router.get("/", response_model=NotificationListResponse)
async def get_notifications(
        user_id: UUID = Depends(get_current_user),
        notificationService: NotificationService = Depends(get_notification_service),
    ):

    return notificationService.get_notifications(user_id)

@router.put("/{id}/read")
async def update_notifications(user_id: UUID):

    return { "data": { "is_read": True }}