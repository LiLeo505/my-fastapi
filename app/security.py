from pwdlib import PasswordHash
import jwt
import os
from dotenv import load_dotenv

from datetime import datetime,timedelta,timezone
from fastapi.security import OAuth2PasswordBearer

password_hash = PasswordHash.recommended()

#JWT配置
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY未配置")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

#将密码哈希处理
def get_password_hash(password: str) -> str:
    return password_hash.hash(password)


#验证密码
def verify_password(plain_password: str, hashed_password: str):
    return password_hash.verify(plain_password, hashed_password)


#创建JWT Token
def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return encoded_jwt


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)

#验证Token
def decode_access_token(token: str):
    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )

    return payload

