from pydantic import BaseModel, EmailStr, Field
class UserModel(BaseModel):
    email:EmailStr = Field(...)
    first_name:str = Field(...)
    last_name:str = Field(...)
    password:str = Field(...)
