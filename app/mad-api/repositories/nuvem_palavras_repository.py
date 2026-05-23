from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.negocio.perguntas import PerguntasModel
from models.negocio.categoria import CategoriaModel
from models.negocio.perguntas_categorias import PerguntasCategoriasModel

class NuvemPalavrasRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_perguntas_para_nuvem(self, filters):
        query = (select(
            PerguntasModel.id,
            PerguntasModel.pergunta,
            PerguntasModel.respcerta,
            CategoriaModel.descricao.label('categoria')
        )
        .join(PerguntasCategoriasModel, PerguntasModel.id == PerguntasCategoriasModel.id_pergunta)
        .join(CategoriaModel, PerguntasCategoriasModel.id_categoria == CategoriaModel.id))

        # Aplicação dos filtros
        if filters.categoria:
            query = query.where(CategoriaModel.descricao == filters.categoria)
        if filters.respcerta:
            query = query.where(PerguntasModel.respcerta == filters.respcerta)

        result = await self.db.execute(query)
        
        return result.all()