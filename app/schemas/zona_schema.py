from pydantic import BaseModel
from typing import Any, Dict

class ZonaCreate(BaseModel):
    nombre: str
    tipo: str
    feature: Dict[str, Any]  # guardamos el Feature completo

class ZonaUpdate(BaseModel):
    nombre: str
    tipo: str
    feature: Dict[str, Any]

class ZonaResponse(BaseModel):
    id: int
    nombre: str
    tipo: str
    feature: Dict[str, Any]

    class Config:
        orm_mode = True