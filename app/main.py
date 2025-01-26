from typing import Union

from fastapi import Depends, FastAPI
from app.routers import users, token
from app.config.db import db

app = FastAPI()

print(db)

@app.get("/")
def read_root():
    return {"success":"true", "description": "Api server is running"}

app.include_router(
    users.router,
    prefix="/users",
    tags=["users"],
)

app.include_router(
    token.router,
    prefix="/token",
    tags=["token"],
)
