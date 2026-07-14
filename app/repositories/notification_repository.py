import json

from fastapi import HTTPException, status
from sqlmodel import Session, text
from uuid import UUID
from app.response_schema.notification_response import NotificationResponse
from app.core.redis import redis_client

class NotificationRepository:
    def __init__(self, session: Session):
        self.session = session


    def get_notifications(self, page: int, limit: int, user_id: UUID):
        conditions = ["user_id = :user_id", "is_read = false"]
        params = {"user_id": user_id}

        params["limit"] = limit
        params["offset"] = (page - 1) * limit

        print('\n \n \n params \n \n \n', params)

        where_clause = " AND ".join(conditions)

        statement = text(
            f"""
            SELECT * FROM notificationmodel
            WHERE {where_clause}
            ORDER BY created_at DESC
            LIMIT :limit OFFSET :offset
            """
        ).bindparams(**params)
    
        rows = self.session.exec(statement).all()
        print('\n \n \n rows \n \n \n', rows)
        return {
            "data": [NotificationResponse(**row._mapping) for row in rows],
        }
    
    def update_read(self, id, user_id: UUID):
        statement = text(
            """
            UPDATE notificationmodel
            SET is_read = true
            WHERE id = :id AND user_id = :user_id
            RETURNING *
            """
        ).bindparams(id=id, user_id=user_id)
    
        result = self.session.exec(statement)
        row = result.first()
        if row is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Notification not found"
            )
        
        self.session.commit()
        redis_client.publish(
            f"notification:{user_id}",
            json.dumps({
                "type": "notification_read",
                "data": { "notification_id": id, "user_id": str(user_id)}
            })
        )
        return NotificationResponse(**dict(row._mapping))
    
    def count(self, user_id: UUID):
        statement = text(
            """
            SELECT count(*) FROM notificationmodel
            WHERE user_id = :user_id AND is_read = false
            """
        ).bindparams(user_id=user_id)
    
        result = self.session.exec(statement)
        row = result.first()

        return {
            "number_of_notification_unread": row[0],
        }
    
    def update_read_all(self, user_id: UUID):
        statement = text(
            """
            UPDATE notificationmodel
            SET is_read = true
            WHERE user_id = :user_id
            """
        ).bindparams(user_id=user_id)
        self.session.exec(statement)
        self.session.commit()

        redis_client.publish(
            f"notification:{user_id}",
            json.dumps({
                "type": "notification_read_all",
                "data": { "user_id": user_id }
            })
        )

        return {"message": "All notifications have been marked as read"}
    
    def delete(self, id: int, user_id: UUID): 
        statement = text(
            """
            DELETE FROM notificationmodel
            WHERE id = :id AND user_id = :user_id
            RETURNING id
            """
        ).bindparams(id=id, user_id=user_id)

        result = self.session.exec(statement)
        row = result.first()

        if row is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Notification not found"
            )
        
        self.session.commit()
        
        redis_client.publish(
            f"notification:{user_id}",
            json.dumps({
                "type": "notification_deleted",
                "data": { "notification_id": id, "user_id": user_id }
            })
        )

        return {"message": "Notification deleted successfully"}