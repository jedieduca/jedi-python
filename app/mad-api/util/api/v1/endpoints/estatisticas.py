import time
from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Request
# from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.usuario_model import UsuarioModel
from models.vwestatistica_avaliacao_model import VwEstatisticaAvaliacoesModel
from models.vwestatistica_categoria_turma_model import VwEstatisticaCategoriaTurmaModel
from models.vwestatististica_partida_turma import VwEstatisticaPartidaTurmaModel
from models.vwdistribuicao_noticias_categoria import VwDistribuicaoNoticiasCategoriaModel

from schemas.estatisticas_schema import EstisticaAvaliacaoFilterSchema, EstisticaCategoriaFilterSchema, EstatisticaPartidaFilterSchema, RespostaEstatisticaSchema, DistribuicaoNotociaCategoriaFilterSchema
from core.deps import get_session_JEDi, get_current_user
from services.data_processing import transforma_em_dataframe, gerar_grafico_avaliacoes, gerar_grafico_categoria_turma, gerar_grafico_partida_escola, gerar_grafico_perfil_noticia

router = APIRouter()

# GET Estatísticas por Avaliação
@router.get(
    '/avaliacao',
    description="""
    Retorna as estatísticas detalhadas por avaliação.

    **Exemplo de chamada via cURL:**
    ```bash
    curl -X 'GET' \\
    'http://localhost:8000/api/v1/estatisticas/avaliacao' \\
        -H 'accept: application/json' \\
        -H 'Authorization: Bearer SEU_TOKEN_AQUI'
    """,
    status_code=status.HTTP_200_OK,
    response_model=RespostaEstatisticaSchema,
    responses={
        200: {
            "description": "Dados retornados com sucesso.",
            "content": {
                "application/json": {
                    "example": {
                        "total": 100,
                        "link_imagem": {"grafico_avaliacao": "http://localhost:8000/static/..."},
                        "dados": []
                    }
                }
            },
        },
        500: {
            "description": "Erro interno durante a chamada.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Mensagem de Erro"
                    }
                }
            },
        }
    }
)
async def get_avaliacoes(
    request: Request,
    filters: EstisticaAvaliacaoFilterSchema = Depends(),
    usuario_logado: UsuarioModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_session_JEDi)
):
    try:
        async with db as session:
            query = select(VwEstatisticaAvaliacoesModel)
            if filters.id:
                query = query.where(VwEstatisticaAvaliacoesModel.id == filters.id)
            if filters.escola:
                query = query.where(VwEstatisticaAvaliacoesModel.escola == filters.escola)
            if filters.turma:
                query = query.where(VwEstatisticaAvaliacoesModel.turma == filters.turma)
            if filters.avaliacao:
                query = query.where(VwEstatisticaAvaliacoesModel.avaliacao == filters.avaliacao)            
            result = await session.execute(query)
            data = result.scalars().all()

        if not data:
            raise HTTPException(detail='Não foi possível gerar os dados.', status_code=status.HTTP_404_NOT_FOUND)
        
        df = await transforma_em_dataframe(data)
      
        # Geração da imagem do gráfico
        await gerar_grafico_avaliacoes(df, "static/estatisticas/img/acertos_avaliacao.jpg")

        # Construímos a URL da imagem
        base_url = str(request.base_url)
        timestamp = int(time.time())
        link = {
            "grafico_avaliacao": f"{base_url}static/estatisticas/img/acertos_avaliacao.jpg?v={timestamp}"
        }
        
        return {
            "total": len(df),
            "link_imagem": link,
            "dados": df.to_dict(orient="records")
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))    
    
# GET Estatísticas por Categoria e Turma
@router.get('/categoria_turma', status_code=status.HTTP_200_OK, response_model=RespostaEstatisticaSchema)
# @cache(expire=300) # Cache de 5 minutos
async def get_categoria_turma(
    request: Request,
    filters: EstisticaCategoriaFilterSchema = Depends(),
    usuario_logado: UsuarioModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_session_JEDi)
):
    try:
        async with db as session:
            query = select(VwEstatisticaCategoriaTurmaModel)
            if filters.id:
                query = query.where(VwEstatisticaCategoriaTurmaModel.id == filters.id)
            if filters.escola:
                query = query.where(VwEstatisticaCategoriaTurmaModel.escola == filters.escola)
            if filters.turma:
                query = query.where(VwEstatisticaCategoriaTurmaModel.turma == filters.turma)
            if filters.categoria:
                query = query.where(VwEstatisticaCategoriaTurmaModel.categoria == filters.categoria)
            result = await session.execute(query)
            data = result.scalars().all()
        if not data:
            raise HTTPException(detail='Não foi possível gerar os dados.', status_code=status.HTTP_404_NOT_FOUND)
        
        df = await transforma_em_dataframe(data)

        await gerar_grafico_categoria_turma(df)
        
        base_url = str(request.base_url)
        timestamp = int(time.time())
        link = {
            "grafico_categoria_turma": f"{base_url}static/estatisticas/img/categoria_turma.png?v={timestamp}"
        }

        return {
            "total": len(df),
            "link_imagem": link,
            "dados": df.to_dict(orient="records")
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))    

# GET Estatísticas por Partida, Escola e Turma
@router.get('/partida_escola', status_code=status.HTTP_200_OK, response_model=RespostaEstatisticaSchema)
# @cache(expire=300) # Cache de 5 minutos
async def get_partida_escola(
    request: Request,
    filters: EstatisticaPartidaFilterSchema = Depends(),
    usuario_logado: UsuarioModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_session_JEDi)
):
    try:
        async with db as session:
            query = select(VwEstatisticaPartidaTurmaModel)
            if filters.id:
                query = query.where(VwEstatisticaPartidaTurmaModel.id == filters.id)
            if filters.escola:
                query = query.where(VwEstatisticaPartidaTurmaModel.escola == filters.escola)
            if filters.turma:
                query = query.where(VwEstatisticaPartidaTurmaModel.turma == filters.turma)
            result = await session.execute(query)
            data = result.scalars().all()
        if not data:
            raise HTTPException(detail='Não foi possível gerar os dados.', status_code=status.HTTP_404_NOT_FOUND)
        
        df = await transforma_em_dataframe(data)

        # 1. Agendamos a geração da imagem para depois da resposta
        await gerar_grafico_partida_escola(df)
        
        # 2. Construímos a URL da imagem
        base_url = str(request.base_url)
        timestamp = int(time.time())
        link = {
            "grafico_escola_turma": f"{base_url}static/estatisticas/img/escola_turma.png?v={timestamp}"
        }

        return {
            "total": len(df),
            "link_imagem": link,
            "dados": df.to_dict(orient="records")
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# GET Estatísticas por Partida, Escola e Turma
@router.get('/perfil_noticia', status_code=status.HTTP_200_OK, response_model=RespostaEstatisticaSchema)
# @cache(expire=300) # Cache de 5 minutos
async def get_perfil_noticia(
    request: Request,
    filters: DistribuicaoNotociaCategoriaFilterSchema = Depends(),
    usuario_logado: UsuarioModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_session_JEDi)
):
    try:
        async with db as session:
            query = select(VwDistribuicaoNoticiasCategoriaModel)
            if filters.id:
                query = query.where(VwDistribuicaoNoticiasCategoriaModel.id == filters.id)
            if filters.categoria:
                query = query.where(VwDistribuicaoNoticiasCategoriaModel.categoria == filters.categoria)
            result = await session.execute(query)
            data = result.scalars().all()
        if not data:
            raise HTTPException(detail='Não foi possível gerar os dados.', status_code=status.HTTP_404_NOT_FOUND)
        
        df = await transforma_em_dataframe(data)

        # 1. Agendamos a geração da imagem para depois da resposta
        await gerar_grafico_perfil_noticia(df)
        
        # 2. Construímos a URL da imagem
        base_url = str(request.base_url)
        timestamp = int(time.time())
        link = {
            "grafico_perfil_noticia": f"{base_url}static/estatisticas/img/perfil_noticia.png?v={timestamp}"
        }

        return {
            "total": len(df),
            "link_imagem": link,
            "dados": df.to_dict(orient="records")
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

