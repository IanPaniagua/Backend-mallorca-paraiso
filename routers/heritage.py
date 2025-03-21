from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
import models
from pydantic import BaseModel, HttpUrl
from datetime import datetime

router = APIRouter()

class HeritageBase(BaseModel):
    name: str
    description: str
    period: str
    highlight: str
    schedule: str
    open_days: str
    image: str
    address: str
    google_maps_url: HttpUrl
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    entrance_fee: Optional[str] = None
    accessibility: Optional[str] = None
    guided_tours: Optional[bool] = None

class HeritageCreate(HeritageBase):
    pass

class Heritage(HeritageBase):
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool

    class Config:
        from_attributes = True

@router.get("/", response_model=List[Heritage])
def get_heritage_sites(
    skip: int = 0,
    limit: int = 100,
    period: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Heritage)
    
    if period:
        query = query.filter(models.Heritage.period == period)
        
    sites = query.offset(skip).limit(limit).all()
    return sites

@router.post("/", response_model=Heritage)
def create_heritage_site(site: HeritageCreate, db: Session = Depends(get_db)):
    db_site = models.Heritage(
        name=site.name,
        description=site.description,
        period=site.period,
        highlight=site.highlight,
        schedule=site.schedule,
        open_days=site.open_days,
        image=site.image,
        address=site.address,
        google_maps_url=str(site.google_maps_url),
        latitude=site.latitude,
        longitude=site.longitude,
        entrance_fee=site.entrance_fee,
        accessibility=site.accessibility,
        guided_tours=site.guided_tours
    )
    db.add(db_site)
    db.commit()
    db.refresh(db_site)
    return db_site

@router.get("/{site_id}", response_model=Heritage)
def get_heritage_site(site_id: int, db: Session = Depends(get_db)):
    site = db.query(models.Heritage).filter(models.Heritage.id == site_id).first()
    if site is None:
        raise HTTPException(status_code=404, detail="Heritage site not found")
    return site

@router.put("/{site_id}", response_model=Heritage)
def update_heritage_site(site_id: int, site: HeritageCreate, db: Session = Depends(get_db)):
    db_site = db.query(models.Heritage).filter(models.Heritage.id == site_id).first()
    if db_site is None:
        raise HTTPException(status_code=404, detail="Heritage site not found")
    
    for key, value in site.dict().items():
        if key == "google_maps_url" and value is not None:
            setattr(db_site, key, str(value))
        else:
            setattr(db_site, key, value)
    
    db.commit()
    db.refresh(db_site)
    return db_site

@router.delete("/{site_id}")
def delete_heritage_site(site_id: int, db: Session = Depends(get_db)):
    db_site = db.query(models.Heritage).filter(models.Heritage.id == site_id).first()
    if db_site is None:
        raise HTTPException(status_code=404, detail="Heritage site not found")
    
    db.delete(db_site)
    db.commit()
    return {"message": "Heritage site deleted successfully"} 