# backend/schemas.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

class EventBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    lat: float
    lon: float
    city_id: int
    description: str = Field(min_length=1, max_length=500)
    status: str = "active"

class EventCreate(EventBase):
    pass

class EventResponse(EventBase):
    id: int
    date: datetime

    model_config = {"from_attributes": True}