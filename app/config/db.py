import asyncio
from app.config.config import settings
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
import logging

import dns.resolver
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']

MONGO_CONNECTION_STRING = f"mongodb+srv://{settings.MONGO_USERNAME}:{settings.MONGO_PASSWORD}@{settings.MONGO_HOST}?retryWrites=true&w=majority&appName=Cluster0"
try:
    client = AsyncIOMotorClient(MONGO_CONNECTION_STRING)
    db = client[settings.MONGO_DATABASE]
    users_collection = db.get_collection("users")
    participants_collection = db.get_collection("participants")
    client.admin.command('ping')
    print("Successfully connected to MongoDB!")
except :
    logging.exception("MongoDB Connection Fail!")
