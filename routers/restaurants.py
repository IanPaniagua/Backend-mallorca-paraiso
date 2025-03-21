from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
import models
from pydantic import BaseModel, HttpUrl
from datetime import datetime

router = APIRouter()

class RestaurantBase(BaseModel):
    nombre: str
    ubicacion: str
    especialidad: str
    precio: str  # "€", "€€", "€€€", "€€€€"
    reserva: bool
    url: Optional[HttpUrl] = None
    tipo: str
    descripcion: Optional[str] = None
    horario: Optional[str] = None
    telefono: Optional[str] = None
    imagen: Optional[str] = None
    latitud: Optional[float] = None
    longitud: Optional[float] = None

class RestaurantCreate(RestaurantBase):
    pass

class Restaurant(RestaurantBase):
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool

    class Config:
        from_attributes = True

@router.get("/", response_model=List[Restaurant])
def get_restaurants(
    skip: int = 0,
    limit: int = 100,
    ubicacion: Optional[str] = None,
    tipo: Optional[str] = None,
    precio: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Restaurant)
    
    if ubicacion:
        query = query.filter(models.Restaurant.ubicacion == ubicacion)
    if tipo:
        query = query.filter(models.Restaurant.tipo == tipo)
    if precio:
        query = query.filter(models.Restaurant.precio == precio)
        
    restaurants = query.offset(skip).limit(limit).all()
    return restaurants

@router.post("/", response_model=Restaurant)
def create_restaurant(restaurant: RestaurantCreate, db: Session = Depends(get_db)):
    db_restaurant = models.Restaurant(
        nombre=restaurant.nombre,
        ubicacion=restaurant.ubicacion,
        especialidad=restaurant.especialidad,
        precio=restaurant.precio,
        reserva=restaurant.reserva,
        url=str(restaurant.url) if restaurant.url else None,
        tipo=restaurant.tipo,
        descripcion=restaurant.descripcion,
        horario=restaurant.horario,
        telefono=restaurant.telefono,
        imagen=restaurant.imagen,
        latitud=restaurant.latitud,
        longitud=restaurant.longitud
    )
    db.add(db_restaurant)
    db.commit()
    db.refresh(db_restaurant)
    return db_restaurant

@router.get("/{restaurant_id}", response_model=Restaurant)
def get_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    restaurant = db.query(models.Restaurant).filter(models.Restaurant.id == restaurant_id).first()
    if restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant

@router.put("/{restaurant_id}", response_model=Restaurant)
def update_restaurant(restaurant_id: int, restaurant: RestaurantCreate, db: Session = Depends(get_db)):
    db_restaurant = db.query(models.Restaurant).filter(models.Restaurant.id == restaurant_id).first()
    if db_restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    for key, value in restaurant.dict().items():
        if key == "url" and value is not None:
            setattr(db_restaurant, key, str(value))
        else:
            setattr(db_restaurant, key, value)
    
    db.commit()
    db.refresh(db_restaurant)
    return db_restaurant

@router.delete("/{restaurant_id}")
def delete_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    db_restaurant = db.query(models.Restaurant).filter(models.Restaurant.id == restaurant_id).first()
    if db_restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    db.delete(db_restaurant)
    db.commit()
    return {"message": "Restaurant deleted successfully"} 