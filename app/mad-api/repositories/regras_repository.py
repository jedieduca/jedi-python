from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.vwapriori_model import VwAprioriModel

class RegrasRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_dados_mineracao(self, filters):
        """Busca todos os registros da view para processamento de regras."""
        async with self.db as session:
            query = select(VwAprioriModel)

            if filters.escola:
                query = query.where(VwAprioriModel.escola == filters.escola)
            if filters.turma:
                query = query.where(VwAprioriModel.turma == filters.turma)
            if filters.capacidade_critica:
                query = query.where(VwAprioriModel.capacidade_critica == filters.capacidade_critica)
            if filters.nome:
                query = query.where(VwAprioriModel.nome == filters.nome)

            result = await session.execute(query)
            
            # Retorna scalars únicos para evitar duplicidade de objetos SQLAlchemy
            return result.scalars().unique().all()