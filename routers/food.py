from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
import models
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class PlatoTipicoBase(BaseModel):
    nombre: str
    categoria: str
    descripcion: str
    ingredientes: List[str]
    imagen: str
    preparacion: Optional[str] = None
    donde_probar: Optional[str] = None
    latitud: Optional[float] = None
    longitud: Optional[float] = None

class PlatoTipicoCreate(PlatoTipicoBase):
    pass

class PlatoTipico(PlatoTipicoBase):
    id: int

    class Config:
        from_attributes = True

@router.get("/", response_model=List[PlatoTipico])
def get_platos(
    skip: int = 0,
    limit: int = 100,
    categoria: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Food)
    
    if categoria:
        query = query.filter(models.Food.categoria == categoria)
        
    platos = query.offset(skip).limit(limit).all()
    
    # Convertir los ingredientes de string a lista
    for plato in platos:
        if isinstance(plato.ingredientes, str):
            plato.ingredientes = plato.ingredientes.split(",")
    
    return platos

@router.post("/", response_model=PlatoTipico)
def create_plato(plato: PlatoTipicoCreate, db: Session = Depends(get_db)):
    # Convertir la lista de ingredientes a string para almacenamiento
    ingredientes_str = ",".join(plato.ingredientes)
    
    db_plato = models.Food(
        nombre=plato.nombre,
        categoria=plato.categoria,
        descripcion=plato.descripcion,
        ingredientes=ingredientes_str,
        imagen=plato.imagen,
        preparacion=plato.preparacion,
        donde_probar=plato.donde_probar,
        latitud=plato.latitud,
        longitud=plato.longitud
    )
    db.add(db_plato)
    db.commit()
    db.refresh(db_plato)
    
    # Convertir ingredientes de vuelta a lista para la respuesta
    db_plato.ingredientes = db_plato.ingredientes.split(",")
    return db_plato

@router.get("/{plato_id}", response_model=PlatoTipico)
def get_plato(plato_id: int, db: Session = Depends(get_db)):
    plato = db.query(models.Food).filter(models.Food.id == plato_id).first()
    
    if plato is None:
        raise HTTPException(status_code=404, detail="Plato no encontrado")
    
    # Convertir ingredientes de string a lista
    if isinstance(plato.ingredientes, str):
        plato.ingredientes = plato.ingredientes.split(",")
    
    return plato

@router.put("/{plato_id}", response_model=PlatoTipico)
def update_plato(plato_id: int, plato: PlatoTipicoCreate, db: Session = Depends(get_db)):
    db_plato = db.query(models.Food).filter(models.Food.id == plato_id).first()
    
    if db_plato is None:
        raise HTTPException(status_code=404, detail="Plato no encontrado")
    
    # Convertir la lista de ingredientes a string
    ingredientes_str = ",".join(plato.ingredientes)
    
    for key, value in plato.dict().items():
        if key == "ingredientes":
            setattr(db_plato, key, ingredientes_str)
        else:
            setattr(db_plato, key, value)
    
    db.commit()
    db.refresh(db_plato)
    
    # Convertir ingredientes de vuelta a lista para la respuesta
    db_plato.ingredientes = db_plato.ingredientes.split(",")
    return db_plato

@router.delete("/{plato_id}")
def delete_plato(plato_id: int, db: Session = Depends(get_db)):
    db_plato = db.query(models.Food).filter(models.Food.id == plato_id).first()
    
    if db_plato is None:
        raise HTTPException(status_code=404, detail="Plato no encontrado")
    
    db.delete(db_plato)
    db.commit()
    return {"message": "Plato eliminado correctamente"} 