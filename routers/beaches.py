from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models import Beach as BeachModel
from pydantic import BaseModel, Field
from datetime import datetime

router = APIRouter()

class BeachBase(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=100)
    imagen: str
    descripcion: str = Field(..., min_length=10)
    zona: str
    pueblo: str
    tipo: str
    servicios: List[str]
    acceso: str
    destacado: bool = False

class BeachCreate(BeachBase):
    pass

class BeachResponse(BeachBase):
    id: int
    last_updated: datetime

    class Config:
        from_attributes = True

@router.get("/", response_model=List[BeachResponse])
def get_beaches(db: Session = Depends(get_db)):
    beaches = db.query(BeachModel).all()
    return beaches

@router.get("/{beach_id}", response_model=BeachResponse)
def get_beach(beach_id: int, db: Session = Depends(get_db)):
    beach = db.query(BeachModel).filter(BeachModel.id == beach_id).first()
    if beach is None:
        raise HTTPException(status_code=404, detail="Playa no encontrada")
    return beach

@router.get("/search/", response_model=List[BeachResponse])
def search_beaches(
    zona: Optional[str] = None,
    pueblo: Optional[str] = None,
    tipo: Optional[str] = None,
    destacado: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    query = db.query(BeachModel)
    
    if zona:
        query = query.filter(BeachModel.zona.ilike(f"%{zona}%"))
    if pueblo:
        query = query.filter(BeachModel.pueblo.ilike(f"%{pueblo}%"))
    if tipo:
        query = query.filter(BeachModel.tipo.ilike(f"%{tipo}%"))
    if destacado is not None:
        query = query.filter(BeachModel.destacado == destacado)
    
    return query.all()

@router.post("/", response_model=BeachResponse)
def create_beach(beach: BeachCreate, db: Session = Depends(get_db)):
    db_beach = BeachModel(**beach.dict())
    db.add(db_beach)
    db.commit()
    db.refresh(db_beach)
    return db_beach

@router.put("/{beach_id}", response_model=BeachResponse)
def update_beach(beach_id: int, beach: BeachCreate, db: Session = Depends(get_db)):
    db_beach = db.query(BeachModel).filter(BeachModel.id == beach_id).first()
    if db_beach is None:
        raise HTTPException(status_code=404, detail="Playa no encontrada")
    
    for key, value in beach.dict().items():
        setattr(db_beach, key, value)
    
    db.commit()
    db.refresh(db_beach)
    return db_beach

@router.delete("/{beach_id}")
def delete_beach(beach_id: int, db: Session = Depends(get_db)):
    db_beach = db.query(BeachModel).filter(BeachModel.id == beach_id).first()
    if db_beach is None:
        raise HTTPException(status_code=404, detail="Playa no encontrada")
    
    db.delete(db_beach)
    db.commit()
    return {"message": "Playa eliminada correctamente"} 