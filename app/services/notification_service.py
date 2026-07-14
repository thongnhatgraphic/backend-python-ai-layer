from uuid import UUID

from app.repositories.notification_repository import NotificationRepository

class NotificationService:
    def __init__(self, repository: NotificationRepository):
        self.repository = repository

    def get_notifications(self, page, limit, user_id: UUID):
        return self.repository.get_notifications(page, limit, user_id)
    
    def update_notification(self, id, user_id: UUID):
        return self.repository.update_read(id, user_id)
    
    def number_of_notifications_unread(self, user_id: UUID):
        return self.repository.count(user_id)
    def read_all_notifications(self, user_id: UUID):
        return self.repository.update_read_all(user_id)
    
    def delete_notification(self, id, user_id: UUID):
        return self.repository.delete(id, user_id)