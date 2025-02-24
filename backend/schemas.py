# backend/schemas.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class EventBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    lat: float
    lon: float
    city_id: int
    description: str = Field(min_length=1, max_length=500)
    status: str = "active"

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):  # Новая модель для частичного обновления
    name: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    city_id: Optional[int] = None
    description: Optional[str] = None
    status: Optional[str] = None

class EventResponse(EventBase):
    id: int
    date: datetime

    model_config = {"from_attributes": True}