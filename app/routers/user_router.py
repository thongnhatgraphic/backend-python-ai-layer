from fastapi import APIRouter, Depends
from sqlmodel import Session
from pydantic import BaseModel

from app.database import get_session
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from app.response_schema.user_schema import UserResponse, UserLoginResponse


router = APIRouter()

def get_user_service(session: Session = Depends(get_session)):
    repoUser = UserRepository(session)
    return UserService(repoUser)

class UserRequest(BaseModel):
    username: str
    password: str
    confirm_password: str

class UserLogin(BaseModel):
    username: str
    password: str

@router.post("/user/register", response_model=UserResponse)
async def register(
        user: UserRequest,
        userService: UserService = Depends(get_user_service)
    ):
    return userService.register(user)

@router.post("/user/login", response_model=UserLoginResponse)
async def login(user: UserLogin, userService: UserService = Depends(get_user_service)):
    return userService.login(user)
