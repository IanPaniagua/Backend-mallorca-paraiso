from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, DateTime, Boolean, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()

# Tabla de asociación para categorías
category_association = Table(
    'category_association',
    Base.metadata,
    Column('item_id', Integer, ForeignKey('items.id')),
    Column('category_id', Integer, ForeignKey('categories.id'))
)

class Beach(Base):
    __tablename__ = "beaches"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    imagen = Column(String(255))
    zona = Column(String(100))
    pueblo = Column(String(100))
    tipo = Column(String(50))
    servicios = Column(Text)  # Almacenado como string separado por comas
    acceso = Column(String(100))
    destacado = Column(Boolean, default=False)
    latitud = Column(Float)
    longitud = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    is_active = Column(Boolean, default=True)

class Monument(Base):
    __tablename__ = "monuments"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    epoca = Column(String(100))
    destacado = Column(String(255))
    horario = Column(String(100))
    imagen = Column(String(255))
    latitud = Column(Float)
    longitud = Column(Float)

class Food(Base):
    __tablename__ = "food"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    categoria = Column(String(100))
    descripcion = Column(Text)
    ingredientes = Column(Text)  # Almacenado como string separado por comas
    imagen = Column(String(255))
    preparacion = Column(Text)
    donde_probar = Column(String(255))
    latitud = Column(Float)
    longitud = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    is_active = Column(Boolean, default=True)

class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    ubicacion = Column(String(100))
    especialidad = Column(String(100))
    precio = Column(String(10))  # "€", "€€", "€€€", "€€€€"
    reserva = Column(Boolean, default=False)
    url = Column(String(255))
    tipo = Column(String(50))
    descripcion = Column(Text)
    horario = Column(String(255))
    telefono = Column(String(20))
    imagen = Column(String(255))
    latitud = Column(Float)
    longitud = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    is_active = Column(Boolean, default=True)

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    items = relationship("Item", secondary=category_association, back_populates="categories")

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    imagen = Column(String)
    descripcion = Column(String)
    zona = Column(String)
    pueblo = Column(String)
    tipo = Column(String)  # "Playa", "Plato", "Monumento", "Restaurante", etc.
    servicios = Column(String)  # Almacenado como string separado por comas
    acceso = Column(String)
    destacado = Column(Boolean, default=False)
    categoria = Column(String)  # Para platos típicos
    ingredientes = Column(String)  # Para platos típicos, almacenado como string separado por comas
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    is_active = Column(Boolean, default=True)
    
    # Relaciones
    categories = relationship("Category", secondary=category_association, back_populates="items")
    reviews = relationship("Review", back_populates="item")

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id"))
    rating = Column(Integer)
    comment = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    item = relationship("Item", back_populates="reviews")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class LocalMarket(Base):
    __tablename__ = "local_markets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    address = Column(String, nullable=False)
    google_maps_url = Column(String, nullable=False)
    days = Column(String, nullable=False)
    hours = Column(String, nullable=False)
    description = Column(Text)
    image = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    is_active = Column(Boolean, default=True) 