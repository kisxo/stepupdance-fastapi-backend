from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from app.utils.auth import ACCESS_TOKEN_EXPIRE_MINUTES, Token, authenticate_user, create_access_token
from datetime import timedelta
from app.models.userModel import UserAuth

router = APIRouter()

@router.post("/")
async def login_for_access_token(user: UserAuth) -> Token:
    user = await authenticate_user(user.phone, user.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect phone or password !",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"phone": user["phone"]}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")