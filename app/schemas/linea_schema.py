from pydantic import BaseModel, Field
from typing import Any, Dict

class LineaCreate(BaseModel):
    nombre: str = Field(..., example="Ruta A")
    tipo: str = Field(..., example="Camino Peatonal")
    feature: Dict[str, Any]

class LineaUpdate(BaseModel):
    nombre: str = Field(..., example="Ruta A")
    tipo: str = Field(..., example="Camino Peatonal")
    feature: Dict[str, Any]

class LineaResponse(BaseModel):
    id: int
    nombre: str
    tipo: str
    feature: Dict[str, Any]

    class Config:
        orm_mode = True