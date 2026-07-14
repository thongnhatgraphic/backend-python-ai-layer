from fastapi import APIRouter, Depends
from sqlmodel import Session
from pydantic import BaseModel
from uuid import UUID

from app.database import get_session
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from app.response_schema.user_schema import UserResponse, UserLoginResponse
from app.services.auth_service import AuthService
from app.repositories.refresh_token_repository import RefreshTokenRepository


router = APIRouter()

def get_user_service(session: Session = Depends(get_session)):
    repo = UserRepository(session)
    return UserService(repo)

def get_auth_service(session: Session = Depends(get_session)):
    refresh_repo = RefreshTokenRepository(session)
    user_repo = UserRepository(session)
    return AuthService(user_repo, refresh_repo )

class UserRequest(BaseModel):
    username: str
    password: str
    confirm_password: str

class UserLogin(BaseModel):
    username: str
    password: str

class LogoutRequest(BaseModel):
    refresh_token: str

class RefreshRequest(BaseModel):
    refresh_token: str


@router.post("/register", response_model=UserResponse)
async def register(
        user: UserRequest,
        userService: UserService = Depends(get_user_service)
    ):
    return userService.register(user)

@router.post("/login", response_model=UserLoginResponse)
async def login(user: UserLogin, authService: AuthService = Depends(get_auth_service)):
    return authService.login(user)

@router.post("/refresh")
async def refresh_access_token(
    body: RefreshRequest,
    authService: AuthService = Depends(get_auth_service)
    ):

    return authService.refresh_access_token(body.refresh_token)

@router.post("/logout")
async def logout(body : LogoutRequest, authService: AuthService = Depends(get_auth_service)):
    return authService.logout(body.refresh_token)

@router.get("/{user_id}/presence")
async def get_presence(user_id: UUID, authService: AuthService = Depends(get_auth_service)):
    return authService.get_presence(user_id)