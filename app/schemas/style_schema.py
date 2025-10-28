
from pydantic import BaseModel
from typing import Optional

class StyleCreate(BaseModel):
    fillColor: Optional[str] = None
    lineColor: Optional[str] = None
    pointColor: Optional[str] = None
    lineWidth: Optional[int] = None
    pointSize: Optional[int] = None

class StyleOut(StyleCreate):
    id: int

    class Config:
        orm_mode = True
