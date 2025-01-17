from typing import Union

from fastapi import Depends, FastAPI
from .routers import users

app = FastAPI()


@app.get("/")
def read_root():
    return {"success":"true", "description": "Api server is running"}

app.include_router(
    users.router,
    prefix="/users",
    tags=["users"],
)