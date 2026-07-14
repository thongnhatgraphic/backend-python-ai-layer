from app.models.user_model import UserModel
from sqlmodel import Session, select
from uuid import UUID
from app.core.redis import redis_client

class UserRepository:
    def __init__(self, session : Session):
        self.session = session

    def create(self, user):
        
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        
        return user
    
    def get_by_username(self, username):
        return self.session.exec(
            select(UserModel)
            .where(UserModel.username == username)
        ).first()
    
    def get_user_by_id(self, id: UUID):
        print("4.8-----\n\n\n----\n\n\n-----", id)

        return self.session.exec(
            select(UserModel)
            .where(UserModel.id == id)
        ).first()
    
    def get_presence(self, user_id: UUID): 
        online = redis_client.get(f"online:user:{user_id}")

        if online :
            return {
                "is_online": True,
                "connection": int(online),
                "last_seen": None,
            }
        
        last_seen = redis_client.get(f"last_seen:user:{user_id}")

        return {
            "is_online": False,
            "connection": None,
            "last_seen": last_seen
        }
