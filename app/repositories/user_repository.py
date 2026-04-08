from app.models.user_model import UserModel
from sqlmodel import Session, select
from uuid import UUID

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

