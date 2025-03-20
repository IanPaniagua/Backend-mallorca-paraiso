from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Monument as MonumentModel
from pydantic import BaseModel

router = APIRouter()

class MonumentBase(BaseModel):
    name: str
    location: str
    description: str
    historical_period: str
    coordinates: str

class MonumentCreate(MonumentBase):
    pass

class MonumentResponse(MonumentBase):
    id: int
    last_updated: str

    class Config:
        from_attributes = True

@router.get("/", response_model=List[MonumentResponse])
def get_monuments(db: Session = Depends(get_db)):
    monuments = db.query(MonumentModel).all()
    return monuments

@router.get("/{monument_id}", response_model=MonumentResponse)
def get_monument(monument_id: int, db: Session = Depends(get_db)):
    monument = db.query(MonumentModel).filter(MonumentModel.id == monument_id).first()
    if monument is None:
        raise HTTPException(status_code=404, detail="Monument not found")
    return monument

@router.get("/search/", response_model=List[MonumentResponse])
def search_monuments(location: str = None, period: str = None, db: Session = Depends(get_db)):
    query = db.query(MonumentModel)
    if location:
        query = query.filter(MonumentModel.location.ilike(f"%{location}%"))
    if period:
        query = query.filter(MonumentModel.historical_period.ilike(f"%{period}%"))
    return query.all() 