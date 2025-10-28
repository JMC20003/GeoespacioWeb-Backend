
from app.core.config import database, global_styles
from app.schemas.style_schema import StyleCreate

class GlobalStyleRepository:
    async def get_global_style(self):
        query = global_styles.select()
        return await database.fetch_one(query)

    async def update_global_style(self, style: StyleCreate):
        query = global_styles.update().values(**style.dict())
        await database.execute(query)
        return await self.get_global_style()
