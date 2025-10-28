
from app.adapters.db.global_style_repo import GlobalStyleRepository
from app.schemas.style_schema import StyleCreate

class GlobalStyleService:
    def __init__(self, repo: GlobalStyleRepository):
        self.repo = repo

    async def get_global_style(self):
        return await self.repo.get_global_style()

    async def update_global_style(self, style: StyleCreate):
        return await self.repo.update_global_style(style)
