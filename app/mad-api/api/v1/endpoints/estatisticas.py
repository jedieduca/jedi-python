import time
from fastapi import APIRouter, status, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from models.usuario_model import UsuarioModel
from schemas.estatisticas_schema import (
    EstisticaAvaliacaoFilterSchema,
    EstisticaCategoriaFilterSchema,
    EstatisticaPartidaFilterSchema,
    RespostaEstatisticaSchema,
    DistribuicaoNotociaCategoriaFilterSchema
)
from services.graficos import GraficosService
from repositories.estatistica_repository import EstatisticaRepository

from core.deps import get_session_JEDi, get_current_user
from core.configs import settings

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
        # Instancia o repositório passando a sessão do banco
        repo = EstatisticaRepository(db)
        
        # Chama a camada de dados de forma isolada
        data = await repo.get_avaliacoes_filtradas(filters)

        if not data:
            raise HTTPException(detail='Não foi possível gerar os dados.', status_code=status.HTTP_404_NOT_FOUND)
    
        path_relativo = "static/estatisticas/img/acertos_avaliacao.jpg"
      
        await GraficosService.criar_grafico_avaliacao(data, path_relativo, filters)
        
        # Construímos a URL da imagem
        base_url = settings.URL_BASE
        timestamp = int(time.time())
        link = {
            "grafico_avaliacao": f"{base_url}/{path_relativo}?v={timestamp}"
        }
        
        return {
            "total": len(data),
            "link_imagem": link,
            "dados": data
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))    
    
# GET Estatísticas por Categoria e Turma
@router.get('/categoria_turma', status_code=status.HTTP_200_OK, response_model=RespostaEstatisticaSchema)
async def get_categoria_turma(
    request: Request,
    filters: EstisticaCategoriaFilterSchema = Depends(),
    usuario_logado: UsuarioModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_session_JEDi)
):
    try:
        # Instancia o repositório passando a sessão do banco
        repo = EstatisticaRepository(db)
        
        # Chama a camada de dados de forma isolada
        data = await repo.get_categorias_filtradas(filters)     
                   
        if not data:
            raise HTTPException(detail='Não foi possível gerar os dados.', status_code=status.HTTP_404_NOT_FOUND)
        
        # Define o caminho onde a imagem será salva
        path_relativo = "static/estatisticas/img/categoria_turma.jpg"
     
        await GraficosService.criar_grafico_categoria(data, path_relativo, filters)

        base_url = settings.URL_BASE
        timestamp = int(time.time())
        link = {
            "grafico_categoria_turma": f"{base_url}/{path_relativo}?v={timestamp}"
        }

        return {
            "total": len(data),
            "link_imagem": link,
            "dados": data
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
        # Instancia o repositório passando a sessão do banco
        repo = EstatisticaRepository(db)
        
        # Chama a camada de dados de forma isolada
        data = await repo.get_partidas_filtradas(filters)
        
        if not data:
            raise HTTPException(detail='Não foi possível gerar os dados.', status_code=status.HTTP_404_NOT_FOUND)

        # Caminho do arquivo
        path_relativo = "static/estatisticas/img/partida_escola.jpg"
        
        await GraficosService.criar_grafico_partida(data, path_relativo, filters)

        # Construímos a URL da imagem
        base_url = settings.URL_BASE
        timestamp = int(time.time())
        link = {
            "grafico_escola_turma": f"{base_url}/{path_relativo}?v={timestamp}"
        }

        return {
            "total": len(data),
            "link_imagem": link,
            "dados": data
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# GET Estatísticas por Partida, Escola e Turma
@router.get('/perfil_noticia', status_code=status.HTTP_200_OK, response_model=RespostaEstatisticaSchema)
async def get_perfil_noticia(
    request: Request,
    filters: DistribuicaoNotociaCategoriaFilterSchema = Depends(),
    usuario_logado: UsuarioModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_session_JEDi)
):
    try:
        # Instancia o repositório passando a sessão do banco
        repo = EstatisticaRepository(db)
        
        # Chama a camada de dados de forma isolada
        data = await repo.get_perfil_noticias_filtradas(filters)      
        
        if not data:
            raise HTTPException(detail='Não foi possível gerar os dados.', status_code=status.HTTP_404_NOT_FOUND)
        
        # Caminho onde a imagem será salva
        path_relativo = "static/estatisticas/img/perfil_noticia.jpg"
        
        await GraficosService.criar_grafico_perfil(data, path_relativo, filters)
        
        # 2. Construímos a URL da imagem
        base_url = settings.URL_BASE
        timestamp = int(time.time())
        print(f"/{path_relativo}?v={timestamp}")
        link = {
            "grafico_perfil_noticia": f"{base_url}/{path_relativo}?v={timestamp}"
        }

        return {
            "total": len(data),
            "link_imagem": link,
            "dados": data
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

