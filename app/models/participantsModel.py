from enum import Enum
from typing import Annotated, List, Optional
from fastapi import HTTPException
from pydantic import ConfigDict, BaseModel, Field, EmailStr
from pydantic.functional_validators import BeforeValidator
from app.config.db import participants_collection
from app.models.eventModel import Event

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

class ParticipantsCollection(BaseModel):
    participants: List[Participant]

async def get_user_participants(id: PyObjectId):
    print(id)
    return ParticipantsCollection(participants = await participants_collection.find({"creator": str(id)}).to_list())
