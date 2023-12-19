'''This file contains helper functions for logging in users with email and password'''
from typing import Annotated
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from models.token import TokenData
from models.database import db
from models.user import UserModel
from config.settings import get_settings

settings = get_settings()
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 180
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password_hash(password: str, hashed: str):
    '''Function to verify password'''
    return pwd_context.verify(password, hashed)


def generate_password_hash(password: str):
    '''Function to generate password'''
    return pwd_context.hash(password)


async def authenticate_user(username: str, password: str)->UserModel|None:
    '''Function to authenticate user'''
    user = await db["users"].find_one({"email": username})
    if not user:
        return None
    user = UserModel.model_construct(user)
    if not verify_password_hash(password, user.password):
        return None
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    '''Function to generate new access tokens'''
    user_data = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=60)
    user_data.update({"exp": expire})
    token = jwt.encode(user_data, settings.APP_SECRET_KEY, algorithm=ALGORITHM)
    return token


async def get_current_user(token:Annotated[str,Depends(oauth2_scheme)])->UserModel:
    ''' function to get currently logged in user'''
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.APP_SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get('sub')
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError as error:
        raise error
    user = await db["users"].find_one({"email":token_data.username})
    user = UserModel.model_construct(user)
    if user is None:
        raise credentials_exception
    return user
