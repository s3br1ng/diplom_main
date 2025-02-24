# backend/crud.py
from sqlalchemy.orm import Session
from . import models, schemas
import logging

logger = logging.getLogger(__name__)

def get_events(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Event).offset(skip).limit(limit).all()

def create_event(db: Session, event: schemas.EventCreate):
    db_event = models.Event(**event.model_dump())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def get_event_by_id(db: Session, event_id: int):
    return db.query(models.Event).filter(models.Event.id == event_id).first()

def update_event_partial(db: Session, event_id: int, updated_data: schemas.EventUpdate):
    db_event = get_event_by_id(db, event_id)
    if not db_event:
        return None

    update_data = updated_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_event, key, value)

    db.commit()
    db.refresh(db_event)
    logger.info(f"Event {event_id} updated with data: {update_data}")
    return db_event

def delete_event(db: Session, event_id: int):
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not db_event:
        return None
    db.delete(db_event)
    db.commit()
    return db_event