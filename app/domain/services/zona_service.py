from app.adapters.db.zona_repo import ZonaRepository
from app.schemas.zona_schema import ZonaCreate, ZonaUpdate

class ZonaService:
    def __init__(self, repo: ZonaRepository):
        self.repo = repo

    async def crear_zona(self, data: ZonaCreate):
        return await self.repo.crear(data.nombre, data.tipo, data.feature)

    async def listar_zonas(self):
        return await self.repo.listar()

    async def obtener_zona(self, id: int):
        return await self.repo.obtener(id)

    async def actualizar_zona(self, id: int, data: ZonaUpdate):
        return await self.repo.actualizar(id, data.nombre, data.tipo, data.feature)

    async def eliminar_zona(self, id: int):
        return await self.repo.eliminar(id)