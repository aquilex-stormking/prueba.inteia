from pydantic import BaseModel
from datetime import date
from typing import Optional
from enum import Enum

class EstadoEvento(str, Enum):
    pendiente = "Pendiente"
    revisado = "Revisado"

class TipoEventoBase(BaseModel):
    id:int
    nombre: str
    class Config:
        orm_mode = True

class TipoEventoCreate(TipoEventoBase):
    nombre:str

class TipoEvento(TipoEventoBase):
    id: int

    class Config:
        orm_mode = True

class EventoBase(BaseModel):
    id:int
    tipo_evento_id: int
    descripcion: str
    fecha: date
    estado: str
    gestion :str
    class Config:
        orm_mode = True

class EventoCreate(EventoBase):
    tipo_evento_id: int
    descripcion: str
    fecha: date
    estado: str 
    gestion :str
    

class Evento(EventoBase):
    id: int

    class Config:
        orm_mode = True
