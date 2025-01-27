from typing import Annotated
from fastapi import APIRouter, Depends
from app.models.userModel import User
from app.models.participantsModel import ParticipantCreate, Participant, get_user_participants
from app.models.eventModel import get_event, Event
from app.utils.auth import get_current_active_user
from app.config.db import participants_collection

router = APIRouter()

@router.get("/")
async def list_participants(current_user: Annotated[User, Depends(get_current_active_user)]):
    return await get_user_participants(current_user["_id"])

@router.post("/")
async def add_participant(
    current_user: Annotated[User, Depends(get_current_active_user)],
    participant_data: ParticipantCreate
):
    if ( event := await get_event(participant_data.detailId)) is None:
        return {"desc": "No event match!\n"}
    
    participant = Participant(
        fname = participant_data.fname,
        age = participant_data.age,
        gender = participant_data.gender,
        detail = event,
        detailId = participant_data.detailId,
        creator = current_user["_id"],
        creator_phone = current_user["phone"],
        payment_amount = event["amount"],
    )

    new_participant = await participants_collection.insert_one(
        participant.model_dump(by_alias=True, exclude=["id"])
    )
    created_participant = await participants_collection.find_one(
        {"_id": new_participant.inserted_id}
    )

    return {'a':"a"}