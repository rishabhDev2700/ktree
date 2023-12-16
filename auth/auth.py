'''
This file contains code for authentication
'''
from typing import Annotated
from fastapi import Body, Depends, FastAPI,HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from models.database import db
from auth.utils import authenticate_user, create_access_token, generate_password_hash, get_current_user
from models.token import Token
from models.user import RegisterUserForm, UserModel

app = FastAPI()


@app.post("/token",response_model=Token)
async def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    '''Login user with OAuth2'''
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token({"sub":user.email})
    return {"access_token": access_token, "token_type":"bearer"}



@app.post("/register",response_model=UserModel)
async def register(form_data:RegisterUserForm=Body(...)):
    '''
    Register New User
    '''
    # email = form_data.email
    # password = form_data.password
    # first_name = form_data.first_name
    # last_name = form_data.last_name
    form_data.password = generate_password_hash(form_data.password)
    new_user = await db["users"].insert_one(form_data.model_dump(by_alias=True,exclude={"id"}))
    user = await db["users"].find_one({"_id":new_user.inserted_id})
    if new_user is not None:
        return UserModel.model_construct(user)
    else:
        raise HTTPException(status_code=403,detail="Could not create user")


@app.get("/test",response_model=UserModel)
async def test(user:Annotated[UserModel,Depends(get_current_user)]):
    '''Test function for testing token'''
    return user
