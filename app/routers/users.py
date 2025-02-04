from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from app.models.userModel import User, UserCreate, UserBase, get_user
from app.config.db import users_collection
from app.utils.auth import get_current_active_user, get_password_hash, check_password_strength
from app.utils.phone import phone_lookup

router = APIRouter()

@router.post(
    "/",
    response_description="Add new user",
    response_model=UserBase,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_user(input_user: UserCreate):
    phone_lookup(input_user.phone)
    check_password_strength(input_user.password)

    if ( await get_user(input_user.phone)) is not None:
        raise HTTPException(status_code=400, detail="User already exists !")
    
    input_user.password = get_password_hash(input_user.password)

    user = User(
        phone= input_user.phone,
        password= input_user.password
    )

    new_user = await users_collection.insert_one(
        user.model_dump(by_alias=True, exclude=["id"])
    )
    created_user = await users_collection.find_one(
        {"_id": new_user.inserted_id}
    )
    return created_user

@router.get("/", response_model=UserBase)
async def check_user(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user

@router.get("/check")
async def check_user(phone: int) -> dict:
    phone_lookup(phone)

    user = await get_user(phone)
    if user is None:
        return {"userExists": False}
    else:
        return {"userExists": True}