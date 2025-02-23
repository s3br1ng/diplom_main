# backend/main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from backend import crud, models, schemas, database
from .database import engine, SessionLocal

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/events/", response_model=schemas.EventResponse)
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    return crud.create_event(db=db, event=event)

@app.get("/events/", response_model=list[schemas.EventResponse])  # Используем list или List
def read_events(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    events = crud.get_events(db, skip=skip, limit=limit)
    return events

@app.put("/events/{event_id}", response_model=schemas.EventResponse)
def update_event(event_id: int, updated_event: schemas.EventCreate, db: Session = Depends(get_db)):
    updated = crud.update_event(db=db, event_id=event_id, updated_event=updated_event)
    if not updated:
        raise HTTPException(status_code=404, detail="Event not found")
    return updated

@app.delete("/events/{event_id}", response_model=schemas.EventResponse)
def delete_event(event_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_event(db=db, event_id=event_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Event not found")
    return deleted