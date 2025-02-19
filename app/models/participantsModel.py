from enum import Enum
from typing import Annotated, List, Optional
from fastapi import HTTPException
from pydantic import ConfigDict, BaseModel, Field, EmailStr
from pydantic.functional_validators import BeforeValidator
from app.config.db import participants_collection
from app.models.eventModel import Event

PyObjectId = Annotated[str, BeforeValidator(str)]

class ParticipantBase(BaseModel):
    eventId: PyObjectId 

class Participant(ParticipantBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    fname: str | None = Field(default=None)
    age: int | None = Field(default=None)
    gender:  str | None = Field(default=None)
    duo_name1: str | None = Field(default=None)
    duo_name2: str | None = Field(default=None)
    group_name: str | None = Field(default=None)
    type: str | None = Field(default=None)
    registered_datetime: str
    creator: PyObjectId
    creator_phone: int
    event_detail: Event
    payment_method: str | None = Field(default=None)
    payment_amount: int
    payment_status: bool = False
    verified: bool = False

class ParticipantsCollection(BaseModel):
    participants: List[Participant]

class GroupParticipantCreate(ParticipantBase):
    type: str = Field(default="group")
    group_name: str
    
class DuoParticipantCreate(ParticipantBase):
    type: str = Field(default="duo") 
    duo_name1: str
    duo_name2: str

class SoloParticipantCreate(ParticipantBase):
    type: str = Field(default="solo")
    fname: str
    age: str
    gender: str

class InputParticipant(BaseModel):
    eventId: PyObjectId
    fname: str | None = Field(default=None, max_length=25)
    age: int | None = Field(default=None)
    gender: str | None = Field(default=None)
    duo_name1: str | None = Field(default=None, max_length=25)
    duo_name2: str | None = Field(default=None, max_length=25)
    group_name: str | None = Field(default=None, max_length=40)

async def get_user_participants(id: PyObjectId):
    return ParticipantsCollection(participants = await participants_collection.find({"creator": str(id)}).to_list())
