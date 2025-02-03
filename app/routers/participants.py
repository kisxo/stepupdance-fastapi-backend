from datetime import datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from app.models.userModel import User
from app.models.participantsModel import SoloParticipantCreate, DuoParticipantCreate, Participant, InputParticipant, get_user_participants, ParticipantsCollection
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
    input_data: InputParticipant
):  
    # check if provided eventId exists 
    if ( event := await get_event(input_data.eventId)) is None:
        raise HTTPException(status_code=404, detail="Selected event not found!")
    
    validate_register_data(input_data, event)

    await check_duplicate(input_data, event, current_user)

    participant = Participant(
        registered_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        creator = str(current_user["_id"]),
        creator_phone = current_user["phone"],
        eventId = str(event["_id"]),
        event_detail = event,
        payment_method = None,
        payment_amount = event["amount"],
        payment_status = False,
        verified  = False
    )
    
    if event["title"] == "Dance Duo":
        participant.type = "duo"
        participant.duo_name1 = input_data.duo_name1
        participant.duo_name2 = input_data.duo_name2
    elif event["title"] == "Dance Group":
        participant.type = "group"
        participant.group_name = input_data.group_name
    else:
        participant.type = "solo"
        participant.fname = input_data.fname
        participant.age = input_data.age
        participant.gender = input_data.gender

    new_participant = await participants_collection.insert_one(
        participant.model_dump(by_alias=True, exclude=["id"])
    )
    created_participant = await participants_collection.find_one(
        {"_id": new_participant.inserted_id}
    )

    return {"detail": "Register Successful"}

def validate_register_data(participant: InputParticipant, event: Event) -> bool:
    if event["title"] == "Dance Duo":
        if participant.duo_name1 is None or participant.duo_name2 is None:
            raise HTTPException(status_code=400, detail="Duo names are required!")
    elif event["title"] == "Dance Group":
        if participant.group_name is None:
            raise HTTPException(status_code=400, detail="Group name is required!")
    else:
        if participant.fname is None or participant.age is None or participant.gender is None:
            raise HTTPException(status_code=400, detail="Full name, age and gender is required!")

    return True

async def check_duplicate(participant: InputParticipant, event: Event, user: User) -> bool:
    query_params: dict
    if event["title"] == "Dance Duo":
        query_params = {
            "creator": str(user["_id"]),
            "eventId": str(event["_id"]),
            "duo_name1": participant.duo_name1,
            "duo_name2": participant.duo_name2,
        }
        
    elif event["title"] == "Dance Group":
        query_params = {
            "creator": str(user["_id"]),
            "eventId": str(event["_id"]),
            "group_name": participant.group_name,
        }
    else:
        query_params = {
            "creator": str(user["_id"]),
            "eventId": str(event["_id"]),
            "fname": participant.fname,
            "age": participant.age,
            "gender": participant.gender,
        }

    query = await participants_collection.find(query_params).to_list()
    if query:
        raise HTTPException(status_code=400, detail="Participant already exists!")
    
    return True