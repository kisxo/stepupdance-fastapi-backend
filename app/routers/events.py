from fastapi import APIRouter
from app.models.eventModel import get_all_events ,get_events_by_category

router = APIRouter()

@router.get("/")
async def create_user():
    return await get_all_events()

@router.get("/{category}")
async def create_user(category):
    return await get_events_by_category(category)