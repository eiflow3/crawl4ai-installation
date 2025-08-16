from fastapi import APIRouter, Body, status
from fastapi.responses import JSONResponse
from typing import List
from config.schemas import User
from config.database import get_users_collection
from utils.encoders import JSONEncoder
import json

router = APIRouter()

@router.get("/users", response_model=List[User])
async def get_all_users():
    """
    Endpoint to get all users from the database.
    """
    users_collection = get_users_collection()
    if users_collection is None:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"error": "Database connection not available"})
    users = list(users_collection.find())
    return JSONResponse(status_code=status.HTTP_200_OK, content=json.loads(JSONEncoder().encode(users)))

@router.post("/users", response_model=User)
async def create_user(user: User = Body(...)):
    """
    Endpoint to create a new user.
    """
    users_collection = get_users_collection()
    if users_collection is None:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"error": "Database connection not available"})
    
    existing_user = users_collection.find_one({"number": user.number})
    if existing_user:
        existing_user["_id"] = str(existing_user["_id"])
        return JSONResponse(status_code=status.HTTP_200_OK, content=existing_user)

    user_dict = user.dict(by_alias=True)
    result = users_collection.insert_one(user_dict)
    user_dict["_id"] = result.inserted_id
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=json.loads(JSONEncoder().encode(user_dict)))

@router.delete("/users", summary="Delete all documents in the Users collection")
async def delete_all_users():
    """
    Deletes all documents from the `users` collection, but keeps the collection itself.
    """
    users_collection = get_users_collection()
    if users_collection is None:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"error": "Database connection not available"})
    
    try:
        result = users_collection.delete_many({})
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": f"Successfully deleted {result.deleted_count} users."})
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"error": f"Failed to delete users: {e}"})
