import uuid

from fastapi import FastAPI, HTTPException, status, Query
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import List, Optional
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from fastapi.encoders import jsonable_encoder

app = FastAPI(
    title="Personal Calendar API",
    description="API for managing personal calendar with MongoDB",
    version="1.0.0"
)

client = MongoClient("mongodb://localhost:27017/")
db = client["personal_calendar"]


# Models
class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: Optional[str] = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "johndoe@example.com",
                "full_name": "John Doe"
            }
        }


class Category(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    name: str = Field(..., min_length=2, max_length=50)
    color: str = Field(..., regex="^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "name": "Work",
                "color": "#FF5733"
            }
        }


class Participant(BaseModel):
    user_id: str
    status: str = Field(..., regex="^(accepted|declined|pending)$")

    class Config:
        arbitrary_types_allowed = True


class Event(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    title: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    location: Optional[str] = None
    category_id: str
    owner_id: str
    participants: List[Participant] = []

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "title": "Team Meeting",
                "description": "Weekly team sync",
                "start_time": "2023-05-20T10:00:00",
                "end_time": "2023-05-20T11:00:00",
                "location": "Conference Room A",
                "category_id": "507f1f77bcf86cd799439011",
                "owner_id": "507f1f77bcf86cd799439012",
                "participants": [
                    {
                        "user_id": "507f1f77bcf86cd799439013",
                        "status": "pending"
                    }
                ]
            }
        }


# CRUD operations for Users
@app.post("/users/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    user_dict = jsonable_encoder(user)
    try:
        db.users.insert_one(user_dict)
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Username or email already exists")
    return user_dict


@app.get("/users/", response_model=List[User])
async def read_users(skip: int = 0, limit: int = 10):
    users = list(db.users.find().skip(skip).limit(limit))
    return users


@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: str):
    if (user := db.users.find_one({"_id": user_id})) is not None:
        return user
    raise HTTPException(status_code=404, detail=f"User {user_id} not found")


@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: str, user: User):
    user_dict = {k: v for k, v in user.dict().items() if v is not None}
    if len(user_dict) >= 1:
        update_result = db.users.update_one(
            {"_id": user_id},
            {"$set": user_dict}
        )
        if update_result.modified_count == 1:
            if (updated_user := db.users.find_one({"_id": user_id})) is not None:
                return updated_user
    if (existing_user := db.users.find_one({"_id": user_id})) is not None:
        return existing_user
    raise HTTPException(status_code=404, detail=f"User {user_id} not found")


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str):
    delete_result = db.users.delete_one({"_id": user_id})
    if delete_result.deleted_count == 1:
        return
    raise HTTPException(status_code=404, detail=f"User {user_id} not found")


# CRUD operations for Categories
@app.post("/categories/", response_model=Category, status_code=status.HTTP_201_CREATED)
async def create_category(category: Category):
    category_dict = jsonable_encoder(category)
    db.categories.insert_one(category_dict)
    return category_dict


@app.get("/categories/", response_model=List[Category])
async def read_categories(skip: int = 0, limit: int = 10):
    categories = list(db.categories.find().skip(skip).limit(limit))
    return categories


@app.get("/categories/{category_id}", response_model=Category)
async def read_category(category_id: str):
    if (category := db.categories.find_one({"_id": category_id})) is not None:
        return category
    raise HTTPException(status_code=404, detail=f"Category {category_id} not found")


@app.put("/categories/{category_id}", response_model=Category)
async def update_category(category_id: str, category: Category):
    category_dict = {k: v for k, v in category.dict().items() if v is not None}
    if len(category_dict) >= 1:
        update_result = db.categories.update_one(
            {"_id": category_id}, {"$set": category_dict}
        )
        if update_result.modified_count == 1:
            if (updated_category := db.categories.find_one({"_id": category_id})) is not None:
                return updated_category
    if (existing_category := db.categories.find_one({"_id": category_id})) is not None:
        return existing_category
    raise HTTPException(status_code=404, detail=f"Category {category_id} not found")


@app.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(category_id: str):
    delete_result = db.categories.delete_one({"_id": category_id})
    if delete_result.deleted_count == 1:
        return
    raise HTTPException(status_code=404, detail=f"Category {category_id} not found")


# CRUD operations for Events
@app.post("/events/", response_model=Event, status_code=status.HTTP_201_CREATED)
async def create_event(event: Event):
    if db.users.find_one({"_id": event.owner_id}) is None:
        raise HTTPException(status_code=400, detail="Owner does not exist")

    if db.categories.find_one({"_id": event.category_id}) is None:
        raise HTTPException(status_code=400, detail="Category does not exist")

    for participant in event.participants:
        if db.users.find_one({"_id": participant.user_id}) is None:
            raise HTTPException(status_code=400, detail=f"Participant {participant.user_id} does not exist")

    event_dict = jsonable_encoder(event)
    db.events.insert_one(event_dict)
    return event_dict


@app.get("/events/", response_model=List[Event])
async def read_events(skip: int = 0, limit: int = 10):
    events = list(db.events.find().skip(skip).limit(limit))
    return events


@app.get("/events/{event_id}", response_model=Event)
async def read_event(event_id: str):
    if (event := db.events.find_one({"_id": event_id})) is not None:
        return event
    raise HTTPException(status_code=404, detail=f"Event {event_id} not found")


@app.put("/events/{event_id}", response_model=Event)
async def update_event(event_id: str, event: Event):
    existing_event = db.events.find_one({"_id": event_id})
    if existing_event is None:
        raise HTTPException(status_code=404, detail=f"Event {event_id} not found")

    if db.users.find_one({"_id": event.owner_id}) is None:
        raise HTTPException(status_code=400, detail="Owner does not exist")

    if db.categories.find_one({"_id": event.category_id}) is None:
        raise HTTPException(status_code=400, detail="Category does not exist")

    for participant in event.participants:
        if db.users.find_one({"_id": participant.user_id}) is None:
            raise HTTPException(status_code=400, detail=f"Participant {participant.user_id} does not exist")

    event_dict = {k: v for k, v in event.dict().items() if v is not None}
    if len(event_dict) >= 1:
        update_result = db.events.update_one(
            {"_id": event_id}, {"$set": event_dict}
        )
        if update_result.modified_count == 1:
            if (updated_event := db.events.find_one({"_id": event_id})) is not None:
                return updated_event
    return existing_event


@app.delete("/events/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(event_id: str):
    delete_result = db.events.delete_one({"_id": event_id})
    if delete_result.deleted_count == 1:
        return
    raise HTTPException(status_code=404, detail=f"Event {event_id} not found")


@app.get("/users/{user_id}/events", response_model=List[Event])
async def get_user_events(
        user_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        skip: int = 0,
        limit: int = 10
):
    if db.users.find_one({"_id": user_id}) is None:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")

    query = {
        "$or": [
            {"owner_id": user_id},
            {"participants.user_id": user_id}
        ]
    }

    if start_date or end_date:
        time_query = {}
        if start_date:
            time_query["$gte"] = start_date
        if end_date:
            time_query["$lte"] = end_date
        query["start_time"] = time_query

    events = list(db.events.find(query).skip(skip).limit(limit))
    return events


@app.patch("/events/{event_id}/participants/{user_id}", response_model=Event)
async def update_participant_status(
        event_id: str,
        user_id: str,
        status: str = Query(..., regex="^(accepted|declined|pending)$")
):
    if db.events.find_one({"_id": event_id}) is None:
        raise HTTPException(status_code=404, detail=f"Event {event_id} not found")

    if db.users.find_one({"_id": user_id}) is None:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")

    update_result = db.events.update_one(
        {
            "_id": event_id,
            "participants.user_id": user_id
        },
        {
            "$set": {"participants.$.status": status}
        }
    )

    if update_result.modified_count == 0:
        raise HTTPException(
            status_code=400,
            detail="Participant not found in event or status not changed"
        )

    if (updated_event := db.events.find_one({"_id": event_id})) is not None:
        return updated_event

    raise HTTPException(status_code=404, detail=f"Event {event_id} not found")

