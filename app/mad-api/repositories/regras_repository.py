from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.vwapriori_model import VwAprioriModel

class RegrasRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_dados_mineracao(self):
        """Busca todos os registros da view para processamento de regras."""
        async with self.db as session:
            query = select(VwAprioriModel)
            
            result = await session.execute(query)
            
            # Retorna scalars únicos para evitar duplicidade de objetos SQLAlchemy
            return result.scalars().unique().all()