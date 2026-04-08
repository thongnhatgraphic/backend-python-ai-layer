from fastapi import HTTPException
from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timedelta, timezone

from app.config import settings

from app.models.user_model import UserModel
from app.repositories.user_repository import UserRepository

from app.utils.security import hash_password
from app.utils.auth import create_access_token

class UserService:
    def __init__(self, 
            repository: UserRepository
        ):
        self.repository = repository

    def register(self, user):
        username = user.username
        password = user.password
        confirm_password = user.confirm_password
        if not username or not password or not confirm_password:
            raise HTTPException(status_code=400, detail="Missing required fields")
        
        if password != confirm_password:
            raise HTTPException(status_code=400, detail="Passwords do not match")
        username = user.username

        if self.repository.get_by_username(username):
            raise HTTPException(status_code=400, detail="Username already exists")

        new_user = UserModel(
            username= username, 
            hashed_password = hash_password(password)
        )
        
        return self.repository.create(new_user)
    