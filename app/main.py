from typing import Union

from fastapi import Depends, FastAPI
from app.routers import users, token, events, participants
from app.config.db import db
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    root_path="/api",
)
origins = [
    "http://localhost:5173",
    "http://localhost:8000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    events.router,
    prefix="/events",
    tags=["events"],
)

app.include_router(
    participants.router,
    prefix="/participants",
    tags=["participants"],
)