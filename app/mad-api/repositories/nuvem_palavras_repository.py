from sqlalchemy import func, literal_column
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.negocio.perguntas import PerguntasModel
from models.negocio.categoria import CategoriaModel
from models.negocio.perguntas_categorias import PerguntasCategoriasModel

class NuvemPalavrasRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_perguntas_para_nuvem(self, filters):
        # Uma linha por notícia, com as categorias agregadas ("A, B"): senão a notícia com várias
        # categorias se repete no grid e tem o texto contado várias vezes na nuvem
        categorias = literal_column(
            "GROUP_CONCAT(DISTINCT categoria.descricao ORDER BY categoria.descricao SEPARATOR ', ')"
        ).label('categoria')

        query = (select(
            PerguntasModel.id,
            PerguntasModel.pergunta,
            PerguntasModel.resp_certa,
            PerguntasModel.analise_proposta,
            PerguntasModel.fala_proposta,
            categorias
        )
        .join(PerguntasCategoriasModel, PerguntasModel.id == PerguntasCategoriasModel.id_pergunta)
        .join(CategoriaModel, PerguntasCategoriasModel.id_categoria == CategoriaModel.id))

        # Aplicação dos filtros
        query = query.where(
            PerguntasModel.analise_proposta.isnot(None),
            PerguntasModel.analise_gpt.isnot(None),
            PerguntasModel.origem_analise.isnot(None),
            PerguntasModel.fala_proposta.isnot(None),
            PerguntasModel.publica == 1,
            PerguntasModel.origem_fala == 1,
        )
        if filters.categoria:
            # Notícias que têm a categoria (a coluna agregada continua mostrando todas as categorias dela)
            com_categoria = (select(PerguntasCategoriasModel.id_pergunta)
                             .join(CategoriaModel, PerguntasCategoriasModel.id_categoria == CategoriaModel.id)
                             .where(CategoriaModel.descricao == filters.categoria))
            query = query.where(PerguntasModel.id.in_(com_categoria))
        if filters.resp_certa:
            query = query.where(PerguntasModel.resp_certa == filters.resp_certa)

        query = query.group_by(PerguntasModel.id, PerguntasModel.pergunta, PerguntasModel.resp_certa,
                               PerguntasModel.analise_proposta, PerguntasModel.fala_proposta)

        result = await self.db.execute(query)
        
        return result.all()