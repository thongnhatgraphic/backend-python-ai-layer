from sqlmodel import Session, text
from uuid import UUID
from app.response_schema.notification_response import NotificationResponse


class NotificationRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self, user_id: UUID):
        statement = text(
            """
            SELECT * FROM notificationmodel
            WHERE user_id = :user_id AND is_read = false
            """
        ).bindparams(user_id=user_id)
    
        rows = self.session.exec(statement).all()
        print('\n \n \n rows \n \n \n', rows)
        return {
            "data": [NotificationResponse(**row._mapping) for row in rows],
        }
    