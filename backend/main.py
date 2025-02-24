# backend/main.py


# backend/.venv/Scripts/Activate.ps1
# uvicorn backend.main:app --reload


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

@app.post("/events/{event_id}/update", response_model=schemas.EventResponse)
def update_event(event_id: int, updated_data: schemas.EventUpdate, db: Session = Depends(get_db)):
    # Исправляем название функции
    updated_event = crud.update_event_partial(db=db, event_id=event_id, updated_data=updated_data)
    if not updated_event:
        raise HTTPException(status_code=404, detail="Event not found")
    return updated_event

@app.delete("/events/{event_id}", response_model=schemas.EventResponse)
def delete_event(event_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_event(db=db, event_id=event_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Event not found")
    return deleted