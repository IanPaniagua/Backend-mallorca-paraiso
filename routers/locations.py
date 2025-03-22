from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
import models
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

# Pydantic models
class LocationBase(BaseModel):
    name: str
    description: Optional[str] = None

class ZoneBase(BaseModel):
    name: str

class ZoneCreate(ZoneBase):
    pass

class MunicipalityCreate(LocationBase):
    zone_id: int

class LocalityBase(BaseModel):
    name: str
    type: models.LocalityType
    zone_id: int

class LocalityCreate(LocalityBase):
    pass

class Zone(ZoneBase):
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool

    class Config:
        from_attributes = True

class Municipality(LocationBase):
    id: int
    zone_id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool

    class Config:
        from_attributes = True

class Locality(LocalityBase):
    id: int
    municipality_id: int
    type: str
    latitude: Optional[float]
    longitude: Optional[float]
    created_at: datetime
    updated_at: datetime
    is_active: bool

    class Config:
        from_attributes = True

# Zone endpoints
@router.get("/zones", response_model=List[Zone])
def get_zones(db: Session = Depends(get_db)):
    return db.query(models.Zone).filter(models.Zone.is_active == True).all()

@router.post("/zones", response_model=Zone)
def create_zone(zone: ZoneCreate, db: Session = Depends(get_db)):
    db_zone = models.Zone(name=zone.name)
    db.add(db_zone)
    db.commit()
    db.refresh(db_zone)
    return db_zone

@router.get("/zones/{zone_id}", response_model=Zone)
def get_zone(zone_id: int, db: Session = Depends(get_db)):
    zone = db.query(models.Zone).filter(models.Zone.id == zone_id).first()
    if zone is None:
        raise HTTPException(status_code=404, detail="Zone not found")
    return zone

@router.put("/zones/{zone_id}", response_model=Zone)
def update_zone(zone_id: int, zone: ZoneCreate, db: Session = Depends(get_db)):
    db_zone = db.query(models.Zone).filter(models.Zone.id == zone_id).first()
    if db_zone is None:
        raise HTTPException(status_code=404, detail="Zone not found")
    
    db_zone.name = zone.name
    db.commit()
    db.refresh(db_zone)
    return db_zone

@router.delete("/zones/{zone_id}")
def delete_zone(zone_id: int, db: Session = Depends(get_db)):
    db_zone = db.query(models.Zone).filter(models.Zone.id == zone_id).first()
    if db_zone is None:
        raise HTTPException(status_code=404, detail="Zone not found")
    
    # Verificar si hay localidades asociadas
    localities = db.query(models.Locality).filter(models.Locality.zone_id == zone_id).first()
    if localities:
        raise HTTPException(status_code=400, detail="Cannot delete zone with associated localities")
    
    db.delete(db_zone)
    db.commit()
    return {"message": "Zone deleted successfully"}

# Municipality endpoints
@router.get("/municipalities/", response_model=List[Municipality])
def get_municipalities(
    zone_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Municipality).filter(models.Municipality.is_active == True)
    if zone_id:
        query = query.filter(models.Municipality.zone_id == zone_id)
    return query.all()

@router.post("/municipalities/", response_model=Municipality)
def create_municipality(municipality: MunicipalityCreate, db: Session = Depends(get_db)):
    # Verify zone exists
    zone = db.query(models.Zone).filter(models.Zone.id == municipality.zone_id).first()
    if not zone:
        raise HTTPException(status_code=404, detail="Zone not found")
    
    db_municipality = models.Municipality(**municipality.dict())
    db.add(db_municipality)
    db.commit()
    db.refresh(db_municipality)
    return db_municipality

# Locality endpoints
@router.get("/localities", response_model=List[Locality])
def get_localities(zone_id: int = None, db: Session = Depends(get_db)):
    query = db.query(models.Locality).filter(models.Locality.is_active == True)
    if zone_id:
        query = query.filter(models.Locality.zone_id == zone_id)
    return query.all()

@router.post("/localities", response_model=Locality)
def create_locality(locality: LocalityCreate, db: Session = Depends(get_db)):
    # Verificar que la zona existe
    zone = db.query(models.Zone).filter(models.Zone.id == locality.zone_id).first()
    if not zone:
        raise HTTPException(status_code=404, detail="Zone not found")

    db_locality = models.Locality(
        name=locality.name,
        type=locality.type,
        zone_id=locality.zone_id
    )
    db.add(db_locality)
    db.commit()
    db.refresh(db_locality)
    return db_locality

@router.get("/localities/{locality_id}", response_model=Locality)
def get_locality(locality_id: int, db: Session = Depends(get_db)):
    locality = db.query(models.Locality).filter(models.Locality.id == locality_id).first()
    if locality is None:
        raise HTTPException(status_code=404, detail="Locality not found")
    return locality

@router.put("/localities/{locality_id}", response_model=Locality)
def update_locality(locality_id: int, locality: LocalityCreate, db: Session = Depends(get_db)):
    db_locality = db.query(models.Locality).filter(models.Locality.id == locality_id).first()
    if db_locality is None:
        raise HTTPException(status_code=404, detail="Locality not found")
    
    # Verificar que la zona existe
    zone = db.query(models.Zone).filter(models.Zone.id == locality.zone_id).first()
    if not zone:
        raise HTTPException(status_code=404, detail="Zone not found")
    
    db_locality.name = locality.name
    db_locality.type = locality.type
    db_locality.zone_id = locality.zone_id
    
    db.commit()
    db.refresh(db_locality)
    return db_locality

@router.delete("/localities/{locality_id}")
def delete_locality(locality_id: int, db: Session = Depends(get_db)):
    db_locality = db.query(models.Locality).filter(models.Locality.id == locality_id).first()
    if db_locality is None:
        raise HTTPException(status_code=404, detail="Locality not found")
    
    # Verificar si hay playas asociadas
    beaches = db.query(models.Beach).filter(models.Beach.locality_id == locality_id).first()
    if beaches:
        raise HTTPException(status_code=400, detail="Cannot delete locality with associated beaches")
    
    db.delete(db_locality)
    db.commit()
    return {"message": "Locality deleted successfully"}

# Nested location information
class LocalityDetail(Locality):
    municipality: Municipality
    zone: Zone

@router.get("/localities/{locality_id}/details", response_model=LocalityDetail)
def get_locality_details(locality_id: int, db: Session = Depends(get_db)):
    """Get detailed information about a locality, including its municipality and zone"""
    locality = db.query(models.Locality).filter(models.Locality.id == locality_id).first()
    if not locality:
        raise HTTPException(status_code=404, detail="Locality not found")
    
    # Add municipality and zone information
    result = LocalityDetail.from_orm(locality)
    result.municipality = Municipality.from_orm(locality.municipality)
    result.zone = Zone.from_orm(locality.municipality.zone)
    return result 