from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from app.models.userModel import User, UserCreate, UserBase, get_user
from app.config.db import users_collection
from app.utils.auth import get_current_active_user, get_password_hash

router = APIRouter()

@router.post(
    "/",
    response_description="Add new user",
    response_model=UserBase,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_user(user: UserCreate):
    if ( await get_user(user.phone)) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists !",
        )
    user.password = get_password_hash(user.password)
    new_student = await users_collection.insert_one(
        user.model_dump(by_alias=True, exclude=["id"])
    )
    created_student = await users_collection.find_one(
        {"_id": new_student.inserted_id}
    )
    return created_student

@router.get("/", response_model=UserBase)
async def check_user(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user

@router.get("/check")
async def check_user(phone: int) -> bool:
    user = await get_user(phone)
    if user is None:
        return False
    else:
        return True