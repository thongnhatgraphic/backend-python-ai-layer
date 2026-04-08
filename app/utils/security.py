from passlib.context import CryptContext
import hashlib

# translate
# crypt context: Bối cảnh mật mã
# schemes: sơ đồ, kế hoạch
# deprecated: đã lỗi thời

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)