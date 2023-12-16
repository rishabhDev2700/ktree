from fastapi import FastAPI
from auth import auth

from routes import nodes

app = FastAPI()
app.mount("/auth",auth.app)
app.include_router(nodes.router,prefix="")
