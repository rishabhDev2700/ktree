from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from auth.token import TokenData
from models.database import db
from config.settings import get_settings

settings = get_settings()
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 180
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password_hash(password: str, hash: str):
    return pwd_context.verify(password, hash)


def generate_password_hash(password: str):
    return pwd_context.hash(password)


async def authenticate_user(username: str, password: str):
    user = await db["users"].find_one({"email": username})
    if not user:
        return False
    if not verify_password_hash(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    user_data = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=60)
    user_data.update({"exp": expire})
    token = jwt.encode(user_data, settings.APP_SECRET_KEY, algorithm=ALGORITHM)
    return token


async def get_current_user(token:Annotated[str,Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.APP_SECRET_KEY, algorithms=ALGORITHM)
        username = payload.get('sub')
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await db['users'].find_one({"email":token_data.username})
    if user is None:
        raise credentials_exception
    return user
