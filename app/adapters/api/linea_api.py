from fastapi import APIRouter, Depends, HTTPException
from app.schemas.linea_schema import LineaCreate, LineaResponse, LineaUpdate
from app.domain.services.linea_service import LineaService
from app.adapters.db.linea_repo import LineaRepository
from app.core.config import database

router = APIRouter(prefix="/lineas", tags=["Líneas"])

def get_service():
    repo = LineaRepository(database)
    service = LineaService(repo)
    return service

@router.post("/", response_model=LineaResponse)
async def crear_linea(linea: LineaCreate, service: LineaService = Depends(get_service)):
    return await service.crear_linea(linea)

@router.get("/", response_model=list[LineaResponse])
async def listar_lineas(service: LineaService = Depends(get_service)):
    return await service.listar_lineas()

@router.get("/{id}", response_model=LineaResponse)
async def obtener_linea(id: int, service: LineaService = Depends(get_service)):
    l = await service.obtener_linea(id)
    if not l:
        raise HTTPException(status_code=404, detail="Línea no encontrada")
    return l

@router.put("/{id}", response_model=LineaResponse)
async def actualizar_linea(id: int, linea: LineaUpdate, service: LineaService = Depends(get_service)):
    updated = await service.actualizar_linea(id, linea)
    if not updated:
        raise HTTPException(status_code=404, detail="Línea no encontrada")
    return updated

@router.delete("/{id}")
async def eliminar_linea(id: int, service: LineaService = Depends(get_service)):
    deleted = await service.eliminar_linea(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Línea no encontrada")
    return {"msg": "Línea eliminada"}