from fastapi import HTTPException
from app.utils.security import hash_password, verify_password
from app.utils.auth import create_access_token

from app.models.user_model import UserModel
from app.response_schema.user_schema import UserLoginResponse

class UserService:
    def __init__(self, repository):
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
    
    def login(self, user):
        username, password = user.username, user.password

        user_by_name = self.repository.get_by_username(username)

        if not user_by_name or not verify_password(password, user_by_name.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        token = create_access_token({
            "sub": str(user_by_name.id), 
            "username": str(user_by_name.username)
        })
        return UserLoginResponse(
            id=user_by_name.id,
            username=user_by_name.username,
            access_token=token,
            created_at=user_by_name.created_at
        )
