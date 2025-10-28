from fastapi import APIRouter, HTTPException
from app.schemas.feature_schema import FeatureCollectionCreate, FeatureCollectionOut, FeatureOut, FeatureCreate
from app.domain.services.feature_service import FeatureService
from app.adapters.db.feature_repo import FeatureRepository

router = APIRouter()
repo = FeatureRepository()
service = FeatureService(repo)

@router.post("/feature/collection")
async def create_feature_collection(fc: FeatureCollectionCreate):
    inserted_count = await service.create_feature_collection(fc)
    return {"message": f"Successfully inserted {inserted_count} features."}

@router.get("/features", response_model=FeatureCollectionOut)
async def get_all_features():
    feature_collection = await service.get_all_features()
    return feature_collection

@router.get("/feature/{id}", response_model=FeatureOut)
async def get_feature_by_id(id: int):
    feature = await service.obtener_por_id(id)
    if not feature:
        raise HTTPException(status_code=404, detail="Feature no encontrado")
    return feature

@router.put("/feature/{id}", response_model=FeatureOut)
async def actualizar_feature(id: int, feature: FeatureCreate):
    feature_actualizado = await service.actualizar(id, feature)
    if not feature_actualizado:
        raise HTTPException(status_code=404, detail="Feature no encontrado")
    return feature_actualizado

@router.delete("/feature/{id}")
async def eliminar_feature(id: int):
    eliminado = await service.eliminar(id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Feature no encontrado")
    return {"mensaje": "Feature eliminado correctamente"}