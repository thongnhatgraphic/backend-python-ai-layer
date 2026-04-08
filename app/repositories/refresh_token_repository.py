from sqlmodel import Session, select
from app.models.refresh_token_model import RefreshTokenModel

class RefreshTokenRepository:
    def __init__(self, session : Session):
        self.session = session
        
    def create(self, token : RefreshTokenModel):
        self.session.add(token)
        self.session.commit()
        self.session.refresh(token)

        return token
    
    def update(self, token : RefreshTokenModel):
        self.session.add(token)
        self.session.commit()
        self.session.refresh(token)

        return token
    
    def get_token_by_user_id(self, user_id : int):
        return self.session.exec(
            select(RefreshTokenModel)
            .where(RefreshTokenModel.user_id == user_id)
        ).first()
    
    def get_by_token(self, token : str):
        return self.session.exec(
            select(RefreshTokenModel)
            .where(RefreshTokenModel.token == token)
        ).first()
    
    def revoke_token(self, token : str):
        tk = self.get_by_token(token)

        if not tk:
            return None
        tk.is_revoked = True
        self.session.add(tk)
        self.session.commit()
        self.session.refresh(tk)
        
        return tk