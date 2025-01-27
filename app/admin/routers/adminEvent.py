from typing import Annotated
from fastapi import APIRouter, Depends
from app.utils.auth import get_current_active_user
from app.models.userModel import User

router = APIRouter()

@router.get("/")
async def read_users_me(
):
    return {"success":"true", "description": "Admin event route is running"}
