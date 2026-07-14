from fastapi import APIRouter, Depends
from pydantic import BaseModel
from uuid import UUID
from sqlmodel import Session

from app.response_schema.notification_response import NotificationListResponse, NotificationResponse
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
        page: int = 1,
        limit: int = 20,
        user_id: UUID = Depends(get_current_user),
        notificationService: NotificationService = Depends(get_notification_service),
    ):

    return notificationService.get_notifications(page, limit, user_id)

@router.put("/{id}/read", response_model=NotificationResponse)
async def update_notifications(
        id: int,
        user_id: UUID = Depends(get_current_user),
        notificationService: NotificationService = Depends(get_notification_service)
    ):

    return notificationService.update_notification(id, user_id)

@router.get("/unread-count")
async def get_number_of_notifications_unread(
        user_id: UUID = Depends(get_current_user),
        notificationService: NotificationService = Depends(get_notification_service)  
    ):
    return notificationService.number_of_notifications_unread(user_id)

@router.put("/read-all")
async def read_all_notifications(
        user_id: UUID = Depends(get_current_user),
        notificationService: NotificationService = Depends(get_notification_service)  
    ):
    return notificationService.read_all_notifications(user_id)

@router.delete("/{id}")
async def delete_notification(
        id: int,
        user_id: UUID = Depends(get_current_user),
        notificationService: NotificationService = Depends(get_notification_service),
    ):
    return notificationService.delete_notification(id, user_id)