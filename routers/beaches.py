from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
import models
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class BeachBase(BaseModel):
    name: str
    image: str
    description: str
    region: str
    town: str
    type: str
    services: List[str]
    access: str
    featured: bool
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class BeachCreate(BeachBase):
    pass

class Beach(BeachBase):
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }

def convert_services_to_list(beach):
    """Helper function to convert services string to list"""
    if isinstance(beach.services, str):
        beach.services = beach.services.split(",") if beach.services else []
    return beach

@router.get("/", response_model=List[Beach])
def get_beaches(
    skip: int = 0,
    limit: int = 100,
    region: Optional[str] = None,
    town: Optional[str] = None,
    type: Optional[str] = None,
    featured: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Beach)
    
    if region:
        query = query.filter(models.Beach.region == region)
    if town:
        query = query.filter(models.Beach.town == town)
    if type:
        query = query.filter(models.Beach.type == type)
    if featured is not None:
        query = query.filter(models.Beach.featured == featured)
        
    beaches = query.offset(skip).limit(limit).all()
    return [convert_services_to_list(beach) for beach in beaches]

@router.post("/", response_model=Beach)
def create_beach(beach: BeachCreate, db: Session = Depends(get_db)):
    db_beach = models.Beach(
        name=beach.name,
        image=beach.image,
        description=beach.description,
        region=beach.region,
        town=beach.town,
        type=beach.type,
        services=",".join(beach.services) if beach.services else "",
        access=beach.access,
        featured=beach.featured,
        latitude=beach.latitude,
        longitude=beach.longitude
    )
    db.add(db_beach)
    db.commit()
    db.refresh(db_beach)
    return convert_services_to_list(db_beach)

@router.get("/{beach_id}", response_model=Beach)
def get_beach(beach_id: int, db: Session = Depends(get_db)):
    beach = db.query(models.Beach).filter(models.Beach.id == beach_id).first()
    if beach is None:
        raise HTTPException(status_code=404, detail="Beach not found")
    return convert_services_to_list(beach)

@router.put("/{beach_id}", response_model=Beach)
def update_beach(beach_id: int, beach: BeachCreate, db: Session = Depends(get_db)):
    db_beach = db.query(models.Beach).filter(models.Beach.id == beach_id).first()
    if db_beach is None:
        raise HTTPException(status_code=404, detail="Beach not found")
    
    # Update all fields
    db_beach.name = beach.name
    db_beach.image = beach.image
    db_beach.description = beach.description
    db_beach.region = beach.region
    db_beach.town = beach.town
    db_beach.type = beach.type
    db_beach.services = ",".join(beach.services) if beach.services else ""
    db_beach.access = beach.access
    db_beach.featured = beach.featured
    db_beach.latitude = beach.latitude
    db_beach.longitude = beach.longitude
    
    db.commit()
    db.refresh(db_beach)
    return convert_services_to_list(db_beach)

@router.delete("/{beach_id}")
def delete_beach(beach_id: int, db: Session = Depends(get_db)):
    db_beach = db.query(models.Beach).filter(models.Beach.id == beach_id).first()
    if db_beach is None:
        raise HTTPException(status_code=404, detail="Beach not found")
    
    db.delete(db_beach)
    db.commit()
    return {"message": "Beach deleted successfully"} 