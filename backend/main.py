# backend/main.py


# backend/.venv/Scripts/Activate.ps1
# uvicorn backend.main:app --reload


from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import crud, models, schemas, auth, database
from datetime import datetime
from typing import List
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#Создает новую сессию базы данных, для работы запросов с дб, потом закрывает
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
#Расшифровывает токен для получения id пользователя, который сверяет с id из БД. Нужна для проверки токена на корректность
async def get_current_user(token: str, db: Session = Depends(get_db)):
    payload = auth.decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    nickname = payload.get("sub")
    user = crud.get_user_by_nickname(db, nickname)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user

#Регистрация аккаунта, проверка ника на уникальность
@app.post("/register", response_model=schemas.UserCreate)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = crud.get_user_by_nickname(db, user.nickname)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nickname already registered")

    created_user = crud.create_user(db=db, user=user)

    return created_user

#Вход пользователя, ник проверяется на уникальность, при входе сохраняет актуальный токен, возвращает токен и его тип
@app.post("/login", response_model=schemas.Token)
def login_user(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.authenticate_user(db, user.nickname, user.password)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect nickname or password")
    access_token = auth.create_access_token({"sub": db_user.nickname})
    return {"access_token": access_token, "token_type": "bearer"}

# Создание мероприятия при помощи токена
@app.post("/events/", response_model=schemas.EventCreate)
def create_event(event: schemas.EventCreate, token: str = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.create_event(db=db, event=event)

#Вывод всех мероприятий, имеющихся в бд
@app.get("/events/", response_model=List[schemas.EventResponse])
def read_events(db: Session = Depends(get_db)):
    events = crud.get_events(db)
    return events

#Обновление мероприятия, проверяет его наличие, проверяет токен на корректность
@app.post("/events/{event_id}/update", response_model=schemas.EventUpdate)
def update_event(
    event_id: int,
    updated_data: schemas.EventUpdate,
    token: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    updated_event = crud.update_event(db=db, event_id=event_id, updated_data=updated_data)
    return updated_event



#Вывод информации о профиле
@app.get("/profile", response_model=schemas.UserProfile)
def get_profile(current_user: models.User = Depends(get_current_user)):
    return {"id": current_user.id, "nickname": current_user.nickname}


#Функция для расшифровки токена и получения информации и профиле
async def get_current_user(token: str = Depends(auth.decode_access_token), db: Session = Depends(get_db)):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    nickname = token.get("nickname")
    if not nickname:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

    user = crud.get_user_by_nickname(db, nickname)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return user