# app/schemas/feature_schema.py
from pydantic import BaseModel, Field
from typing import Any, List, Dict, Optional

class FeatureCreate(BaseModel):
    type: str
    properties: Dict[str, Any] = Field(default_factory=dict)
    geometry: Dict[str, Any]
    id: Optional[int] = None

class FeatureCollectionCreate(BaseModel):
    type: str
    features: List[FeatureCreate]

# Schemas for output
class FeatureOut(BaseModel):
    id: int
    type: str = "Feature"
    geometry: Dict[str, Any]
    properties: Dict[str, Any]

class FeatureCollectionOut(BaseModel):
    type: str = "FeatureCollection"
    features: List[FeatureOut]
