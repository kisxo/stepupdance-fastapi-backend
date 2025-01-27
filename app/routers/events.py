from fastapi import APIRouter
from app.models.eventModel import get_all_events ,get_events_by_category

router = APIRouter()

@router.get("/")
async def list_all_events():
    return await get_all_events()

@router.get("/{category}")
async def list_events_by_category(category):
    return await get_events_by_category(category)