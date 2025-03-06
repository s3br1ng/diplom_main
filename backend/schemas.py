# backend/schemas.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

#Модель для создания мероприятия
class EventBase(BaseModel):
    name: str
    lat: float
    lon: float
    city_id: int
    description: str
    status: str

#Модель для создания мероприятия
class EventCreate(EventBase):
    pass

#Модель для обновления данных мероприятия
class EventUpdate(BaseModel):
    name: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    city_id: Optional[int] = None
    description: Optional[str] = None
    status: Optional[str] = None

class EventResponse(EventBase):
    id: int
    date: datetime

#Модель для регистрации нового пользователя
class UserCreate(BaseModel):
    nickname: str
    password: str = Field(min_length=6)

#Модель для входа пользователя
class UserLogin(BaseModel):
    nickname: str
    password: str

#Модель для получения токена и его типа
class Token(BaseModel):
    access_token: str
    token_type: str

class UserProfile(BaseModel):
    id: int
    nickname: str
