''' Data models for token and token data'''
from pydantic import BaseModel, EmailStr, Field


class Token(BaseModel):
    '''Token model with access token'''
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    '''Token Model for decoded tokens'''
    username:EmailStr = Field(...)
    