from fastapi import APIRouter, Depends, HTTPException
from app.schemas.zona_schema import ZonaCreate, ZonaResponse, ZonaUpdate
from app.domain.services.zona_service import ZonaService
from app.adapters.db.zona_repo import ZonaRepository
from app.core.config import database

router = APIRouter(prefix="/zonas", tags=["Zonas"])

# Dependencia
def get_service():
    repo = ZonaRepository(database)
    service = ZonaService(repo)
    return service

@router.post("/", response_model=ZonaResponse)
async def crear_zona(zona: ZonaCreate, service: ZonaService = Depends(get_service)):
    return await service.crear_zona(zona)

@router.get("/", response_model=list[ZonaResponse])
async def listar_zonas(service: ZonaService = Depends(get_service)):
    return await service.listar_zonas()

@router.get("/{id}", response_model=ZonaResponse)
async def obtener_zona(id: int, service: ZonaService = Depends(get_service)):
    z = await service.obtener_zona(id)
    if not z:
        raise HTTPException(status_code=404, detail="Zona no encontrada")
    return z

@router.put("/{id}", response_model=ZonaResponse)
async def actualizar_zona(id: int, zona: ZonaUpdate, service: ZonaService = Depends(get_service)):
    z = await service.actualizar_zona(id, zona)
    if not z:
        raise HTTPException(status_code=404, detail="Zona no encontrada")
    return z

@router.delete("/{id}")
async def eliminar_zona(id: int, service: ZonaService = Depends(get_service)):
    eliminado = await service.eliminar_zona(id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Zona no encontrada")
    return {"msg": "Zona eliminada correctamente"}
