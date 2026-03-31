from app.models.user_model import UserModel
from sqlmodel import Session, select


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

