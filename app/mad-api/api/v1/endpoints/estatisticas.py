import time
from fastapi import APIRouter, status, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from models.usuario_model import UsuarioModel
from schemas.estatisticas_schema import (
    EstisticaAvaliacaoFilterSchema,
    EstisticaCategoriaFilterSchema,
    EstatisticaPartidaFilterSchema,
    RankingMatchesFilterSchema,
    RespostaEstatisticaSchema,
    DistribuicaoNotociaCategoriaFilterSchema,
    PerfilEscolaFilterSchema,
    CapacidadeCriticaFilterSchema,
    AnaliseIdadeFilterSchema,
    AutoavaliacaoJogoFilterSchema,
)
from services.graficos import GraficosService
from repositories.estatistica_repository import EstatisticaRepository

from core.deps import get_session_JEDi, get_current_user
from core.configs import settings

router = APIRouter()

# Resposta 200 sem dados: o cliente exibe a mensagem como aviso, não como erro
def resposta_vazia(mensagem: str = 'Nenhum registro encontrado para os filtros selecionados.',
                   nivel: str = 'info') -> dict:
    return {"total": 0, "link_imagem": {}, "dados": [], "nivel": nivel, "mensagem": mensagem}

# GET Estatísticas por Avaliação
@router.get('/avaliacao', status_code=status.HTTP_200_OK, response_model=RespostaEstatisticaSchema)
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
            return resposta_vazia()
    
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
    except HTTPException:
        raise    
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
            return resposta_vazia()
        
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
    except HTTPException:
        raise    
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
            return resposta_vazia()

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
    except HTTPException:
        raise    
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
            return resposta_vazia()
        
        # Caminho onde a imagem será salva
        path_relativo = "static/estatisticas/img/perfil_noticia.jpg"
        
        await GraficosService.criar_grafico_perfil(data, path_relativo, filters)
        
        # 2. Construímos a URL da imagem
        base_url = settings.URL_BASE
        timestamp = int(time.time())
        # print(f"/{path_relativo}?v={timestamp}")
        link = {
            "grafico_perfil_noticia": f"{base_url}/{path_relativo}?v={timestamp}"
        }

        return {
            "total": len(data),
            "link_imagem": link,
            "dados": data
        }
    except HTTPException:
        raise            
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get('/ranking_partidas', status_code=status.HTTP_200_OK, response_model=RespostaEstatisticaSchema)
async def get_ranking_partidas(
    request: Request,
    filters: RankingMatchesFilterSchema = Depends(),
    usuario_logado: UsuarioModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_session_JEDi)
):
    try:
        repo = EstatisticaRepository(db)
        data = await repo.get_ranking_partidas_aluno(filters)
        
        if not data:
            return resposta_vazia()

        path_relativo = "static/estatisticas/img/ranking_partidas.jpg"
        
        await GraficosService.criar_grafico_ranking_partidas(data, path_relativo)

        base_url = settings.URL_BASE
        timestamp = int(time.time())
        link = {
            "grafico_ranking_partidas": f"{base_url}/{path_relativo}?v={timestamp}"
        }

        return {
            "total": len(data),
            "link_imagem": link,
            "dados": data
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get('/perfil_escolas', status_code=status.HTTP_200_OK, response_model=RespostaEstatisticaSchema)
async def get_perfil_escolas(
    request: Request,
    filters: PerfilEscolaFilterSchema = Depends(),
    usuario_logado: UsuarioModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_session_JEDi)
):
    try:
        repo = EstatisticaRepository(db)
        data = await repo.get_perfil_escolas_filtradas(filters)
        
        if not data:
            return resposta_vazia()

        path_relativo = "static/estatisticas/img/perfil_escolas.jpg"
        
        await GraficosService.criar_grafico_perfil_escolas(data, path_relativo, filters)

        base_url = settings.URL_BASE
        timestamp = int(time.time())
        link = {
            "grafico_perfil_escolas": f"{base_url}/{path_relativo}?v={timestamp}"
        }

        return {
            "total": len(data),
            "link_imagem": link,
            "dados": data
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get('/capacidade_critica', status_code=status.HTTP_200_OK, response_model=RespostaEstatisticaSchema)
async def get_capacidade_critica(
    request: Request,
    filters: CapacidadeCriticaFilterSchema = Depends(),
    usuario_logado: UsuarioModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_session_JEDi)
):
    try:
        repo = EstatisticaRepository(db)
        data = await repo.get_capacidade_critica_filtrada(filters)
        
        if not data:
            return resposta_vazia()

        path_relativo = "static/estatisticas/img/capacidade_critica.jpg"
        
        await GraficosService.criar_grafico_capacidade_critica(data, path_relativo, filters)

        base_url = settings.URL_BASE
        timestamp = int(time.time())
        link = {
            "grafico_capacidade_critica": f"{base_url}/{path_relativo}?v={timestamp}"
        }

        return {
            "total": len(data),
            "link_imagem": link,
            "dados": data
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get('/analise_idade', status_code=status.HTTP_200_OK, response_model=RespostaEstatisticaSchema)
async def get_analise_idade(
    request: Request,
    filters: AnaliseIdadeFilterSchema = Depends(),
    usuario_logado: UsuarioModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_session_JEDi)
):
    try:
        repo = EstatisticaRepository(db)
        data = await repo.get_analise_idade_filtrada(filters)

        if not data:
            return resposta_vazia()

        # O boxplot precisa de pelo menos um jogador com idade informada
        if all(item.idade is None for item in data):
            return resposta_vazia('Nenhum jogador com idade informada para os filtros selecionados.', nivel='warning')

        path_relativo = "static/estatisticas/img/analise_idade.jpg"

        await GraficosService.criar_grafico_analise_idade(data, path_relativo, filters)

        base_url = settings.URL_BASE
        timestamp = int(time.time())
        link = {
            "grafico_analise_idade": f"{base_url}/{path_relativo}?v={timestamp}"
        }

        return {
            "total": len(data),
            "link_imagem": link,
            "dados": data
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get('/autoavaliacao_jogo', status_code=status.HTTP_200_OK, response_model=RespostaEstatisticaSchema)
async def get_autoavaliacao_jogo(
    request: Request,
    filters: AutoavaliacaoJogoFilterSchema = Depends(),
    usuario_logado: UsuarioModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_session_JEDi)
):
    try:
        repo = EstatisticaRepository(db)
        data = await repo.get_autoavaliacao_jogo_filtrada(filters)

        if not data:
            return resposta_vazia()

        path_relativo = "static/estatisticas/img/autoavaliacao_jogo.jpg"

        await GraficosService.criar_grafico_autoavaliacao_jogo(data, path_relativo, filters)

        base_url = settings.URL_BASE
        timestamp = int(time.time())
        link = {
            "grafico_autoavaliacao_jogo": f"{base_url}/{path_relativo}?v={timestamp}"
        }

        return {
            "total": len(data),
            "link_imagem": link,
            "dados": data
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
