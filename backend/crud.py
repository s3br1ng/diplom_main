from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext

#Используется для хэширования паролей 
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#Поиск пользователя по нику
def get_user_by_nickname(db: Session, nickname: str):
    return db.query(models.User).filter(models.User.nickname == nickname).first()

#Создание нового пользователя в бд
def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(nickname=user.nickname, password_hash=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

#Проверка введенного пароля с действующим паролем
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

#Вход пользователя. Если пользователь не найден или пароль несовпадает, то возвращает none
def authenticate_user(db: Session, nickname: str, password: str):
    user = get_user_by_nickname(db, nickname)
    if not user or not verify_password(password, user.password_hash):
        return None
    return user

#Возвращает все мероприятия
def get_events(db: Session):
    return db.query(models.Event)

#Создает новое мероприятие
def create_event(db: Session, event: schemas.EventCreate):
    db_event = models.Event(**event.model_dump())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

#Поиск мероприятия по id
def get_event_by_id(db: Session, event_id: int):
    return db.query(models.Event).filter(models.Event.id == event_id).first()

#Обновление существующего события
def update_event(db: Session, event_id: int, updated_data: schemas.EventUpdate):
    db_event = get_event_by_id(db, event_id)
    if not db_event:
        return None

    update_data = updated_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_event, key, value)

    db.commit()
    db.refresh(db_event)
    return db_event
