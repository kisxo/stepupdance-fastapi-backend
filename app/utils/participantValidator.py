from fastapi import HTTPException
from app.models.eventModel import Event
from app.models.participantsModel import InputParticipant
from app.models.userModel import User
from app.config.db import participants_collection


def validate_input_data(participant: InputParticipant, event: Event) -> bool:
    if event["title"] == "Dance Duo":
        if participant.duo_name1 is None or participant.duo_name2 is None:
            raise HTTPException(status_code=400, detail="Duo names are required!")
        else:
            participant.duo_name1 = participant.duo_name1.title()
            participant.duo_name2 = participant.duo_name2.title()

    elif event["title"] == "Dance Group":
        if participant.group_name is None:
            raise HTTPException(status_code=400, detail="Group name is required!")
        else:
            participant.group_name = participant.group_name.title()
        
    else:
        if participant.fname is None or participant.age is None or participant.gender not in ["male", "female"]:
            raise HTTPException(status_code=400, detail="Full name, age and gender is required!")
        else:
            participant.fname = participant.fname.title()

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

def verify_requirements(participant: InputParticipant, event: Event, user: User) -> bool:
    if event["title"] == "Dance Solo":
        verify_name(participant.fname)
        verify_age(participant.age)

    elif event["title"] == "Dance Duo":
        verify_name(participant.duo_name1)
        verify_name(participant.duo_name2)

    elif event["title"] == "Dance Group":
        verify_name(participant.group_name)
        
    else:
        verify_name(participant.fname)
        verify_age(participant.age)

    return True
       
def verify_name(name: str) -> bool:
    if (len(name) < 6):
        raise HTTPException(status_code=400, detail="Enter full name !")

    if name.replace(" ", "").isalpha() == True:
        return True
    else:
        raise HTTPException(status_code=400, detail="Enter full name !")
    
def verify_age(age: int, min: int= 4, max: int= 50) -> bool:
    if(age < min or age > max):
        raise HTTPException(status_code=400, detail="Participant age is invalid!")
    
    return True
    