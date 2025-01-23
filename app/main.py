from typing import Union

from fastapi import Depends, FastAPI
from .routers import users

import os
from dotenv import load_dotenv, dotenv_values 
from bson import ObjectId
import motor.motor_asyncio
from pymongo import ReturnDocument
import dns.resolver
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']

load_dotenv()

app = FastAPI()

client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])

@app.get("/")
def read_root():
    return {"success":"true", "description": "Api server is running"}

app.include_router(
    users.router,
    prefix="/users",
    tags=["users"],
)
