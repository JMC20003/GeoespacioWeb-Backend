from app.adapters.db.punto_repo import PuntoRepository
from app.schemas.punto_schema import PuntoCreate, PuntoUpdate

class PuntoService:
    def __init__(self, repo: PuntoRepository):
        self.repo = repo

    async def crear(self, data: PuntoCreate):
        return await self.repo.crear(data.nombre, data.feature)

    async def listar(self):
        return await self.repo.listar()

    async def obtener(self, id: int):
        return await self.repo.obtener(id)

    async def actualizar(self, id: int, data: PuntoUpdate):
        return await self.repo.actualizar(id, data.nombre, data.feature)

    async def eliminar(self, id: int):
        return await self.repo.eliminar(id)