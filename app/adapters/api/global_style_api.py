from fastapi import APIRouter, HTTPException
from app.schemas.style_schema import StyleCreate, StyleOut
from app.domain.services.global_style_service import GlobalStyleService
from app.adapters.db.global_style_repo import GlobalStyleRepository

router = APIRouter()
repo = GlobalStyleRepository()
service = GlobalStyleService(repo)

@router.get("/style", response_model=StyleOut)
async def get_global_style():
    style = await service.get_global_style()
    if not style:
        raise HTTPException(status_code=404, detail="Global style not found")
    return style

@router.put("/style", response_model=StyleOut)
async def update_global_style(style: StyleCreate):
    updated_style = await service.update_global_style(style)
    if not updated_style:
        raise HTTPException(status_code=404, detail="Global style not found")
    return updated_style
