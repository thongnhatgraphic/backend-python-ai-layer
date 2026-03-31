from jose import jwt
from datetime import datetime, timedelta, timezone

from jose import jwt
from datetime import datetime, timedelta
from config import settings

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, "secret", algorithm="HS256")
    print("encoded_jwt", encoded_jwt)
    return encoded_jwt