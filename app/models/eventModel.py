from typing import Annotated, List, Optional
from bson import ObjectId
from pydantic import BaseModel, BeforeValidator, Field
from app.config.db import events_collection

PyObjectId = Annotated[str, BeforeValidator(str)]

class Event(BaseModel):    
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    title: str
    category: str
    amount: int
    group: str | None = None
    date: str | None = None
    description: str | None = None

class EventsCollection(BaseModel):
    events: List[Event]

async def get_events_by_category(category: str):
    return EventsCollection(events = await events_collection.find({"category": category}).to_list(50))

async def get_all_events():
    return EventsCollection(events = await events_collection.find().to_list(50))

async def get_event(id: str):
    if ( event := await events_collection.find_one(ObjectId(id))) is not None:
        return event
