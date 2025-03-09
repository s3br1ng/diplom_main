from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

#Модель для создания мероприятия
class EventBase(BaseModel):
    id: int
    name: str
    lat: float
    lon: float
    city_id: int
    description: str
    status: str
    date: datetime

#Модель для обновления данных мероприятия
class EventUpdate(BaseModel):
    name: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    city_id: Optional[int] = None
    description: Optional[str] = None
    status: Optional[str] = None


#Модель для входа пользователя
class UserLogin(BaseModel):
    nickname: str
    password: str = Field(min_length=6)

#Модель для получения токена и его типа
class Token(BaseModel):
    access_token: str
    token_type: str

#Модель для получения информации о профиле
class UserProfile(BaseModel):
    id: int
    nickname: str
