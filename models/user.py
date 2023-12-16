from typing import Optional
from pydantic import BaseModel, EmailStr, Field

from models.database import PyObjectId
class UserModel(BaseModel):
    '''User Model for users'''
    id:Optional[PyObjectId] = Field(alias='_id',default=None)
    email:EmailStr = Field(...)
    first_name:str = Field(...)
    last_name:str = Field(...)
    password:str = Field(...)
    is_verified:bool = Field(default=False)
    verification_code:Optional[str] = Field(...)

class RegisterUserForm(BaseModel):
    '''Form model for registering users'''
    email:EmailStr = Field(...)
    first_name:str = Field(...)
    last_name:str = Field(...)
    password:str = Field(...)
    
    