from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.vwestatistica_avaliacao_model import VwEstatisticaAvaliacoesModel
from models.vwestatistica_categoria_turma_model import VwEstatisticaCategoriaTurmaModel
from models.vwestatististica_partida_turma import VwEstatisticaPartidaTurmaModel
from models.vwdistribuicao_noticias_categoria import VwDistribuicaoNoticiasCategoriaModel

class EstatisticaRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_avaliacoes_filtradas(self, filters):
        query = select(VwEstatisticaAvaliacoesModel)
        
        if filters.id:
            query = query.where(VwEstatisticaAvaliacoesModel.id == filters.id)
        if filters.escola:
            query = query.where(VwEstatisticaAvaliacoesModel.escola == filters.escola)
        if filters.turma:
            query = query.where(VwEstatisticaAvaliacoesModel.turma == filters.turma)
        if filters.avaliacao:
            query = query.where(VwEstatisticaAvaliacoesModel.avaliacao == filters.avaliacao)
            
        result = await self.db.execute(query)
        
        return result.scalars().all()
    
    async def get_categorias_filtradas(self, filters):
        query = select(VwEstatisticaCategoriaTurmaModel)
        
        if filters.id:
            query = query.where(VwEstatisticaCategoriaTurmaModel.id == filters.id)
        if filters.escola:
            query = query.where(VwEstatisticaCategoriaTurmaModel.escola == filters.escola)
        if filters.turma:
            query = query.where(VwEstatisticaCategoriaTurmaModel.turma == filters.turma)
        if filters.categoria:
            query = query.where(VwEstatisticaCategoriaTurmaModel.categoria == filters.categoria)
        
        result = await self.db.execute(query)
        
        return result.scalars().all()

    async def get_partidas_filtradas(self, filters):
        query = select(VwEstatisticaPartidaTurmaModel)
        
        if filters.id:
            query = query.where(VwEstatisticaPartidaTurmaModel.id == filters.id)
        if filters.escola:
            query = query.where(VwEstatisticaPartidaTurmaModel.escola == filters.escola)
        if filters.turma:
            query = query.where(VwEstatisticaPartidaTurmaModel.turma == filters.turma)
            
        result = await self.db.execute(query)
        
        return result.scalars().all()
    
    async def get_perfil_noticias_filtradas(self, filters):
        query = select(VwDistribuicaoNoticiasCategoriaModel)
        
        if filters.id:
            query = query.where(VwDistribuicaoNoticiasCategoriaModel.id == filters.id)
        if filters.categoria:
            query = query.where(VwDistribuicaoNoticiasCategoriaModel.categoria == filters.categoria)
        
        result = await self.db.execute(query)
        
        return result.scalars().all()
