from fastapi import APIRouter, Depends, HTTPException
from app.schemas.punto_schema import PuntoCreate, PuntoResponse, PuntoUpdate
from app.domain.services.punto_service import PuntoService
from app.adapters.db.punto_repo import PuntoRepository
from app.core.config import database


router = APIRouter(prefix="/puntos", tags=["Puntos"])

def get_service() -> PuntoService:
    repo = PuntoRepository(database)
    return PuntoService(repo)

@router.post("/", response_model=PuntoResponse)
async def crear_punto(data: PuntoCreate, service: PuntoService = Depends(get_service)):
    return await service.crear(data)

@router.get("/", response_model=list[PuntoResponse])
async def listar_puntos(service: PuntoService = Depends(get_service)):
    return await service.listar()

@router.get("/{id}", response_model=PuntoResponse)
async def obtener_punto(id: int, service: PuntoService = Depends(get_service)):
    punto = await service.obtener(id)
    if not punto:
        raise HTTPException(status_code=404, detail="Punto no encontrado")
    return punto

@router.put("/{id}", response_model=PuntoResponse)
async def actualizar_punto(id: int, data: PuntoUpdate, service: PuntoService = Depends(get_service)):
    punto = await service.actualizar(id, data)
    if not punto:
        raise HTTPException(status_code=404, detail="Punto no encontrado")
    return punto

@router.delete("/{id}")
async def eliminar_punto(id: int, service: PuntoService = Depends(get_service)):
    eliminado = await service.eliminar(id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Punto no encontrado")
    return {"mensaje": "Punto eliminado correctamente"}