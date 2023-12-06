from pydantic import BaseModel, EmailStr, Field

class TokenData(BaseModel):
    username:EmailStr = Field(...)