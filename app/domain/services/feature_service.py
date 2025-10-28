# app/domain/services/feature_service.py
from app.adapters.db.feature_repo import FeatureRepository
from app.schemas.feature_schema import FeatureCollectionCreate, FeatureCreate

class FeatureService:
    def __init__(self, repo: FeatureRepository):
        self.repo = repo

    async def create_feature_collection(self, feature_collection: FeatureCollectionCreate):
        count = await self.repo.create_feature_collection(feature_collection.features)
        return count

    async def get_all_features(self):
        features_list = await self.repo.get_all_features()
        return {"type": "FeatureCollection", "features": features_list}

    async def eliminar(self, id: int) -> bool:
        return await self.repo.eliminar(id)

    async def obtener_por_id(self, id: int):
        return await self.repo.obtener_por_id(id)

    async def actualizar(self, id: int, feature: FeatureCreate):
        return await self.repo.actualizar(id, feature)