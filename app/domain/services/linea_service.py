from app.adapters.db.linea_repo import LineaRepository
from app.schemas.linea_schema import LineaCreate, LineaUpdate

class LineaService:
    def __init__(self, repo: LineaRepository):
        self.repo = repo

    async def crear_linea(self, data: LineaCreate):
        return await self.repo.crear(data.nombre, data.tipo, data.feature)

    async def listar_lineas(self):
        return await self.repo.listar()

    async def obtener_linea(self, id):
        return await self.repo.obtener(id)

    async def actualizar_linea(self, id, data: LineaUpdate):
        return await self.repo.actualizar(id, data.nombre, data.tipo, data.feature)

    async def eliminar_linea(self, id: int) -> bool:
        return await self.repo.eliminar(id)
