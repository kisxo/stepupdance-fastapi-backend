from typing import Annotated, Optional
from fastapi import HTTPException
from pydantic import ConfigDict, BaseModel, Field, EmailStr
from pydantic.functional_validators import BeforeValidator
from app.config.db import users_collection

# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]

class UserBase(BaseModel):
    phone: int

class User(UserBase):
    # The primary key for the user Model, stored as a `str` on the instance.
    # This will be aliased to `_id` when sent to MongoDB,
    # but provided as `id` in the API requests and responses.
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    password: str
    admin: bool = Field(default=False)
    verified: bool = Field(default=False)
    disabled: bool = Field(default=False)

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    phone: int | None = None
    password: str | None = None

class UserAuth(BaseModel):
    phone: int
    password: str

async def get_user(phone: int):
    if ( user := await users_collection.find_one({"phone": phone})) is not None:
        return user