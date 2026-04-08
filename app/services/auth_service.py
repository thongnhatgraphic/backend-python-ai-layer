from fastapi import HTTPException
from sqlmodel import Session
from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timedelta, timezone

from app.utils.security import verify_password
from app.config import settings
from app.repositories.user_repository import UserRepository
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.utils.auth import create_access_token, create_refresh_token
from app.models.refresh_token_model import RefreshTokenModel

class AuthService:
    def __init__(self, 
        user_repo: UserRepository,
        refresh_token_repo: RefreshTokenRepository
    ):  
        self.user_repo = user_repo
        self.refresh_token_repo = refresh_token_repo

    def refresh(self, refresh_token : str):
        try:
            print("3-----\n\n\n----\n\n\n-----")
            payload = jwt.decode(
                refresh_token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
            print("4-----\n\n\n----\n\n\n-----", payload)


            if payload.get("type") != "refresh_token":
                HTTPException(status_code=401, detail="Invalid token type")

            db_token = self.refresh_token_repo.get_by_token(refresh_token)

            if not db_token:
                HTTPException(status_code=401, detail="Token Not Found")

            if db_token.is_revoked:
                HTTPException(status_code=401, detail="Token Revoked")

            if db_token.expires_at < datetime.now(timezone.utc):
                HTTPException(status_code=401, detail="Token Expired")

            user_id = payload.get("sub")
            username = payload.get("username")

            if not user_id or not username:
                HTTPException(status_code=401, detail="Invalid token payload")

            new_access_token = create_access_token({
                "sub": user_id,
                "username": username,
                "type": "access_token"
            })

            return {"access_token": new_access_token}

        except JWTError:
            return HTTPException(status_code=401, detail=JWTError)

    def login(self, user):
        username = user.username
        password = user.password

        user_by_name = self.user_repo.get_by_username(username)
    
        if not user_by_name or not verify_password(password, user_by_name.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        access_token = create_access_token({
            "sub": str(user_by_name.id), 
            "username": str(user_by_name.username),
            "type": "access_token"
        })

        refresh_token = create_refresh_token({
            "sub": str(user_by_name.id), 
            "username": str(user_by_name.username),
            "type": "refresh_token"
        })

        refresh_token_obj = RefreshTokenModel(
            user_id=user_by_name.id,
            token=refresh_token,
            expires_at=datetime.now(timezone.utc) + timedelta(days=7)
        )

        self.refresh_token_repo.create(refresh_token_obj)

        return {
            "id": user_by_name.id,
            "username": user_by_name.username,
            "created_at": user_by_name.created_at,
            "access_token": access_token, 
            "refresh_token": refresh_token
            }

    def logout(self, refresh_token : str):
        db_token = self.refresh_token_repo.get_by_token(refresh_token)

        if not db_token:
            raise HTTPException(status_code=401, detail="Token Not Found")

        self.refresh_token_repo.revoke_token(refresh_token)

        return {"message": "Logout successful"}
    
    def refresh_access_token(self, refresh_token : str):
        try:
            payload = jwt.decode(
                refresh_token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
            
            if payload.get("type") != "refresh_token":
                raise HTTPException(status_code=401, detail="Invalid token type")
            
            db_token = self.refresh_token_repo.get_by_token(refresh_token)
                  
            if not db_token:
                raise HTTPException(status_code=401, detail="Token Not Found")

            if db_token.is_revoked:
                raise HTTPException(status_code=401, detail="Token Revoked")

            if db_token.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
                raise HTTPException(status_code=401, detail="Token Expired")
            # 🔥 1. Revoke token cũ
            db_token.is_revoked = True

            self.refresh_token_repo.update(db_token)

            user_id = payload.get("sub")
            username = payload.get("username")
            

            user = self.user_repo.get_by_username(username)
            if not user:
                raise HTTPException(status_code=401, detail="User Not Found")

            if not user_id or not username:
                raise HTTPException(status_code=401, detail="Invalid token payload")

            # 🔥 2. Tạo refresh token mới (ROTATE)
            new_refresh_token = create_refresh_token({
                "sub": str(user.id),
                "username": user.username,
                "type": "refresh_token"
            })

            new_access_token = create_access_token({
                "sub": str(user.id),
                "username": user.username,
                "type": "access_token"
            })

            new_refresh_token_obj = RefreshTokenModel(
                user_id=user.id,
                token=new_refresh_token,
                expires_at=datetime.now(timezone.utc) + timedelta(days=7)
            )

            self.refresh_token_repo.create(new_refresh_token_obj)

            return {
                "access_token": new_access_token,
                "refresh_token": new_refresh_token  # 🔥 quan trọng
            }

        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")