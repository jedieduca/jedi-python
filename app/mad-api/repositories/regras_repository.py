from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.vwapriori_model import VwAprioriModel

class RegrasRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_dados_mineracao(self, filters):
        """Busca todos os registros da view para processamento de regras."""
        async with self.db as session:
            query = select(*VwAprioriModel.__table__.columns)

            if filters.escola:
                query = query.where(VwAprioriModel.escola == filters.escola)
            if filters.turma:
                query = query.where(VwAprioriModel.turma == filters.turma)
            if filters.capacidade_critica:
                query = query.where(VwAprioriModel.capacidade_critica == filters.capacidade_critica)
            if filters.nome:
                query = query.where(VwAprioriModel.nome == filters.nome)

            query = query.order_by(*VwAprioriModel.__table__.columns)
            result = await session.execute(query)
            
            # Retorna cada linha da view como dict (sem colapsar por id)
            return [dict(row) for row in result.mappings().all()]