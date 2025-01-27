from enum import Enum
from typing import Annotated, Optional
from fastapi import HTTPException
from pydantic import ConfigDict, BaseModel, Field, EmailStr
from pydantic.functional_validators import BeforeValidator
from app.config.db import users_collection
from app.models.eventModel import Event

# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]

class ParticipantBase(BaseModel):
    fname: str
    age: int
    gender: str
    detailId: PyObjectId

class Participant(ParticipantBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    creator: PyObjectId
    creator_phone: int
    detail: Event
    payment_amount: int
    payment_status: bool = False

class ParticipantCreate(ParticipantBase):
    pass
