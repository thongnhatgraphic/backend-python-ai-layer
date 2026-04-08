from app.config import settings

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from jose import jwt, JWTError

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException
from uuid import UUID

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    try:
        token = credentials.credentials
        
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        if payload.get("type") != "access_token":
            raise HTTPException(status_code=401, detail="Invalid token type")
        
        user_id: str = payload.get("sub")
        print(f"\n \n ----::User ID::---> {user_id} \n \n")

        if not payload:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        return UUID(user_id)

    except JWTError as e:
        print("JWT ERROR:", str(e))
        raise HTTPException(status_code=401, detail="Invalid token")