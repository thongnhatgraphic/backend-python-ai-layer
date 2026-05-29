from uuid import UUID

from app.repositories.notification_repository import NotificationRepository

class NotificationService:
    def __init__(self, repository: NotificationRepository):
        self.repository = repository

    def get_notifications(self, user_id: UUID):
        return self.repository.get_all(user_id)