from fastapi import APIRouter, Depends
from sqlmodel import Session
from pydantic import BaseModel

from app.database import get_session
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService


router = APIRouter()

def get_user_service(session: Session = Depends(get_session)):
    repoUser = UserRepository(session)
    return UserService(repoUser)

class UserRequest(BaseModel):
    username: str
    password: str
    confirm_password: str

@router.post("/user/register")
async def register(
        user: UserRequest,
        userService: UserService = Depends(get_user_service)
    ):
    return userService.register(user)

@router.post("/user/login")
async def login():
    return {
        "message": "Login successfully",
        "data": {
            "username": "Nhat",
            "password": "123456"
        }
    }

@router.get("/user")
async def get_user():
    return {
        "message": "User information",
        "data": {
            "username": "Nhat",
            "password": "123456"
        }
    }