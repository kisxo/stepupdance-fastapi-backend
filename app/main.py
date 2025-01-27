from typing import Union

from fastapi import Depends, FastAPI
from app.routers import users, token, participants
from app.config.db import db
from app.admin.routers import adminEvent

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

app.include_router(
    adminEvent.router,
    prefix="/adminEvent",
    tags=["adminEvent"],
)