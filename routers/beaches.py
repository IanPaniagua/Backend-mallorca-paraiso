from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
import models
from pydantic import BaseModel, validator
from datetime import datetime
from utils.geo import calculate_distance, is_point_in_mallorca
from sqlalchemy import func

router = APIRouter()

class ZoneResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class LocalityResponse(BaseModel):
    id: int
    name: str
    type: models.LocalityType
    zone: ZoneResponse

    class Config:
        from_attributes = True

class BeachBase(BaseModel):
    name: str
    image: str
    description: str
    category: models.CoastalLocationType
    type: models.BeachType
    services: List[str]
    access: str
    featured: bool
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    locality_id: int

    @validator('services', pre=True)
    def split_services(cls, v):
        if isinstance(v, str):
            return v.split(',') if v else []
        return v

    @validator('latitude')
    def validate_latitude(cls, v):
        if v is not None and (v < 39.2 or v > 40.0):
            raise ValueError('Latitude must be within Mallorca bounds (39.2 to 40.0)')
        return v

    @validator('longitude')
    def validate_longitude(cls, v):
        if v is not None and (v < 2.2 or v > 3.5):
            raise ValueError('Longitude must be within Mallorca bounds (2.2 to 3.5)')
        return v

class BeachCreate(BeachBase):
    pass

class Beach(BeachBase):
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool
    locality: LocalityResponse
    distance: Optional[float] = None

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
    locality_id: Optional[int] = None,
    category: Optional[models.CoastalLocationType] = None,
    type: Optional[models.BeachType] = None,
    featured: Optional[bool] = None,
    latitude: Optional[float] = Query(None, description="User's latitude for distance calculation"),
    longitude: Optional[float] = Query(None, description="User's longitude for distance calculation"),
    max_distance: Optional[float] = Query(None, description="Maximum distance in kilometers"),
    order_by_distance: bool = Query(False, description="Order results by distance from user's location"),
    db: Session = Depends(get_db)
):
    query = db.query(models.Beach).filter(models.Beach.is_active == True)
    
    if locality_id:
        query = query.filter(models.Beach.locality_id == locality_id)
    if category:
        query = query.filter(models.Beach.category == category)
    if type:
        query = query.filter(models.Beach.type == type)
    if featured is not None:
        query = query.filter(models.Beach.featured == featured)

    beaches = []
    if latitude is not None and longitude is not None:
        if not is_point_in_mallorca(latitude, longitude):
            raise HTTPException(
                status_code=400,
                detail="Coordinates must be within Mallorca bounds"
            )
        
        db_beaches = query.all()
        
        for beach in db_beaches:
            if beach.latitude and beach.longitude:
                distance = calculate_distance(
                    latitude, longitude,
                    beach.latitude, beach.longitude
                )
                
                if max_distance is not None and distance > max_distance:
                    continue
                
                beach_dict = Beach.from_orm(beach)
                beach_dict.distance = distance
                beaches.append(beach_dict)
        
        if order_by_distance:
            beaches.sort(key=lambda x: x.distance)
        
        beaches = beaches[skip:skip + limit]
    else:
        beaches = query.offset(skip).limit(limit).all()
        beaches = [Beach.from_orm(beach) for beach in beaches]

    return [convert_services_to_list(beach) for beach in beaches]

@router.get("/nearby", response_model=List[Beach])
def get_nearby_beaches(
    latitude: float = Query(..., description="User's latitude"),
    longitude: float = Query(..., description="User's longitude"),
    radius: float = Query(5.0, description="Search radius in kilometers"),
    limit: int = Query(10, description="Maximum number of results to return"),
    db: Session = Depends(get_db)
):
    """
    Find beaches within a specified radius from the given coordinates,
    ordered by distance.
    """
    if not is_point_in_mallorca(latitude, longitude):
        raise HTTPException(
            status_code=400,
            detail="Coordinates must be within Mallorca bounds"
        )

    # Obtener todas las playas activas con coordenadas
    query = db.query(models.Beach).filter(
        models.Beach.is_active == True,
        models.Beach.latitude.isnot(None),
        models.Beach.longitude.isnot(None)
    )

    beaches = []
    for beach in query.all():
        distance = calculate_distance(
            latitude, longitude,
            beach.latitude, beach.longitude
        )
        
        if distance <= radius:
            beach_dict = Beach.from_orm(beach)
            beach_dict.distance = distance
            beaches.append(beach_dict)

    # Ordenar por distancia y limitar resultados
    beaches.sort(key=lambda x: x.distance)
    beaches = beaches[:limit]

    return [convert_services_to_list(beach) for beach in beaches]

@router.post("/", response_model=Beach)
def create_beach(beach: BeachCreate, db: Session = Depends(get_db)):
    # Verificar que la localidad existe
    locality = db.query(models.Locality).filter(models.Locality.id == beach.locality_id).first()
    if not locality:
        raise HTTPException(status_code=404, detail="Locality not found")

    db_beach = models.Beach(
        name=beach.name,
        image=beach.image,
        description=beach.description,
        category=beach.category,
        type=beach.type,
        services=",".join(beach.services) if beach.services else "",
        access=beach.access,
        featured=beach.featured,
        latitude=beach.latitude,
        longitude=beach.longitude,
        locality_id=beach.locality_id
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
    
    # Verificar que la localidad existe
    locality = db.query(models.Locality).filter(models.Locality.id == beach.locality_id).first()
    if not locality:
        raise HTTPException(status_code=404, detail="Locality not found")
    
    # Update all fields
    db_beach.name = beach.name
    db_beach.image = beach.image
    db_beach.description = beach.description
    db_beach.category = beach.category
    db_beach.type = beach.type
    db_beach.services = ",".join(beach.services) if beach.services else ""
    db_beach.access = beach.access
    db_beach.featured = beach.featured
    db_beach.latitude = beach.latitude
    db_beach.longitude = beach.longitude
    db_beach.locality_id = beach.locality_id
    
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