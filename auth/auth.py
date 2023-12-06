from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordRequestForm

from auth.utils import authenticate_user, create_access_token

app = FastAPI()


@app.get("")
async def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends]):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token({"sub":user.email})
    return {"access_token": access_token, "token_type":"bearer"}



@app.post("")
async def register():
    pass
