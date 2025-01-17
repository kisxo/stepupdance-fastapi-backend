from fastapi import APIRouter

router = APIRouter()

# dev route
@router.get("/")
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]
