from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
import models
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class BeachBase(BaseModel):
    nombre: str
    imagen: str
    descripcion: str
    zona: str
    pueblo: str
    tipo: str = "Playa"
    servicios: List[str]
    acceso: str
    destacado: bool = False
    latitud: Optional[float] = None
    longitud: Optional[float] = None

class BeachCreate(BeachBase):
    pass

class Beach(BeachBase):
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool

    class Config:
        from_attributes = True

@router.get("/", response_model=List[Beach])
def get_playas(
    skip: int = 0,
    limit: int = 100,
    zona: Optional[str] = None,
    destacado: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Beach)
    
    if zona:
        query = query.filter(models.Beach.zona == zona)
    if destacado is not None:
        query = query.filter(models.Beach.destacado == destacado)
        
    playas = query.offset(skip).limit(limit).all()
    
    # Convertir los servicios de string a lista
    for playa in playas:
        if isinstance(playa.servicios, str):
            playa.servicios = playa.servicios.split(",")
    
    return playas

@router.post("/", response_model=Beach)
def create_playa(playa: BeachCreate, db: Session = Depends(get_db)):
    # Convertir la lista de servicios a string para almacenamiento
    servicios_str = ",".join(playa.servicios)
    
    db_playa = models.Beach(
        nombre=playa.nombre,
        imagen=playa.imagen,
        descripcion=playa.descripcion,
        zona=playa.zona,
        pueblo=playa.pueblo,
        tipo=playa.tipo,
        servicios=servicios_str,
        acceso=playa.acceso,
        destacado=playa.destacado,
        latitud=playa.latitud,
        longitud=playa.longitud
    )
    db.add(db_playa)
    db.commit()
    db.refresh(db_playa)
    
    # Convertir servicios de vuelta a lista para la respuesta
    db_playa.servicios = db_playa.servicios.split(",")
    return db_playa

@router.get("/{playa_id}", response_model=Beach)
def get_playa(playa_id: int, db: Session = Depends(get_db)):
    playa = db.query(models.Beach).filter(models.Beach.id == playa_id).first()
    
    if playa is None:
        raise HTTPException(status_code=404, detail="Playa no encontrada")
    
    # Convertir servicios de string a lista
    if isinstance(playa.servicios, str):
        playa.servicios = playa.servicios.split(",")
    
    return playa

@router.put("/{playa_id}", response_model=Beach)
def update_playa(playa_id: int, playa: BeachCreate, db: Session = Depends(get_db)):
    db_playa = db.query(models.Beach).filter(models.Beach.id == playa_id).first()
    
    if db_playa is None:
        raise HTTPException(status_code=404, detail="Playa no encontrada")
    
    # Convertir la lista de servicios a string
    servicios_str = ",".join(playa.servicios)
    
    for key, value in playa.dict().items():
        if key == "servicios":
            setattr(db_playa, key, servicios_str)
        else:
            setattr(db_playa, key, value)
    
    db.commit()
    db.refresh(db_playa)
    
    # Convertir servicios de vuelta a lista para la respuesta
    db_playa.servicios = db_playa.servicios.split(",")
    return db_playa

@router.delete("/{playa_id}")
def delete_playa(playa_id: int, db: Session = Depends(get_db)):
    db_playa = db.query(models.Beach).filter(models.Beach.id == playa_id).first()
    
    if db_playa is None:
        raise HTTPException(status_code=404, detail="Playa no encontrada")
    
    db.delete(db_playa)
    db.commit()
    return {"message": "Playa eliminada correctamente"} 