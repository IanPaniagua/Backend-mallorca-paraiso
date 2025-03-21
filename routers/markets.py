from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
import models
from pydantic import BaseModel, HttpUrl
from datetime import datetime

router = APIRouter()

class LocalMarketBase(BaseModel):
    name: str
    location: str
    address: str
    google_maps_url: HttpUrl
    days: str
    hours: str
    description: Optional[str] = None
    image: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class LocalMarketCreate(LocalMarketBase):
    pass

class LocalMarket(LocalMarketBase):
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool

    class Config:
        from_attributes = True

@router.get("/", response_model=List[LocalMarket])
def get_markets(
    skip: int = 0,
    limit: int = 100,
    location: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.LocalMarket)
    
    if location:
        query = query.filter(models.LocalMarket.location == location)
        
    markets = query.offset(skip).limit(limit).all()
    return markets

@router.post("/", response_model=LocalMarket)
def create_market(market: LocalMarketCreate, db: Session = Depends(get_db)):
    db_market = models.LocalMarket(
        name=market.name,
        location=market.location,
        address=market.address,
        google_maps_url=str(market.google_maps_url),
        days=market.days,
        hours=market.hours,
        description=market.description,
        image=market.image,
        latitude=market.latitude,
        longitude=market.longitude
    )
    db.add(db_market)
    db.commit()
    db.refresh(db_market)
    return db_market

@router.get("/{market_id}", response_model=LocalMarket)
def get_market(market_id: int, db: Session = Depends(get_db)):
    market = db.query(models.LocalMarket).filter(models.LocalMarket.id == market_id).first()
    if market is None:
        raise HTTPException(status_code=404, detail="Local market not found")
    return market

@router.put("/{market_id}", response_model=LocalMarket)
def update_market(market_id: int, market: LocalMarketCreate, db: Session = Depends(get_db)):
    db_market = db.query(models.LocalMarket).filter(models.LocalMarket.id == market_id).first()
    if db_market is None:
        raise HTTPException(status_code=404, detail="Local market not found")
    
    for key, value in market.dict().items():
        if key == "google_maps_url" and value is not None:
            setattr(db_market, key, str(value))
        else:
            setattr(db_market, key, value)
    
    db.commit()
    db.refresh(db_market)
    return db_market

@router.delete("/{market_id}")
def delete_market(market_id: int, db: Session = Depends(get_db)):
    db_market = db.query(models.LocalMarket).filter(models.LocalMarket.id == market_id).first()
    if db_market is None:
        raise HTTPException(status_code=404, detail="Local market not found")
    
    db.delete(db_market)
    db.commit()
    return {"message": "Local market deleted successfully"} 