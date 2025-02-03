

from fastapi import HTTPException

from app.models.eventModel import Event
from app.models.participantsModel import InputParticipant
from app.models.userModel import User
from app.config.db import participants_collection


def validate_input_data(participant: InputParticipant, event: Event) -> bool:
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