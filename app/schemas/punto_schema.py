from pydantic import BaseModel, Field
from typing import Any, Dict

class PuntoCreate(BaseModel):
    nombre: str = Field(..., example="Plaza Vea San Isidro")
    feature: Dict[str, Any]

class PuntoUpdate(BaseModel):
    nombre: str = Field(..., example="Plaza Vea San Isidro")
    feature: Dict[str, Any]

class PuntoResponse(BaseModel):
    id: int
    nombre: str
    feature: Dict[str, Any]

    class Config:
        orm_mode = True