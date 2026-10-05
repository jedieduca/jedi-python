import time 
from fastapi import APIRouter, status, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from models.usuario_model import UsuarioModel
from repositories.regras_repository import RegrasRepository
from services.regras import RegrasService
from schemas.vwapriori_schema import RespostaApriorSchema, RegrasAssociacaorFilterSchema
from core.deps import get_session_JEDi, get_current_user
from core.configs import settings

router = APIRouter(redirect_slashes=False)

# Resposta 200 sem dados: o cliente exibe a mensagem como aviso, não como erro
def resposta_vazia(mensagem: str, nivel: str = 'info') -> dict:
    return {"total_regras": 0, "links_imagens": {}, "regras": [], "nivel": nivel, "mensagem": mensagem}

# GET Regras
@router.get('', status_code=status.HTTP_200_OK, response_model=RespostaApriorSchema)
async def get_rules(
    request: Request,
    filters: RegrasAssociacaorFilterSchema = Depends(),
    usuario_logado: UsuarioModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_session_JEDi)
):
    try:
        # Instancia o repositório passando a sessão do banco e a camada de serviços
        repo     = RegrasRepository(db)
        service  = RegrasService()
        
        # Chama a camada de dados de forma isolada
        data = await repo.get_dados_mineracao(filters)

        if not data:
            return resposta_vazia('Nenhum registro encontrado para os filtros selecionados.')

        regras, links_imagens = await service.processar_regras_associacao(data, filters)

        if not regras:
            return resposta_vazia('Nenhuma regra de associação encontrada para os parâmetros atuais.')

        # Formatação de URLs de saída
        base_url = settings.URL_BASE
        timestamp = int(time.time())
        links_formatados = {
            key: f"{base_url}/{value}?v={timestamp}" 
            for key, value in links_imagens.items()
        }

        return {
            "total_regras": len(regras),
            "links_imagens": links_formatados,
            "regras": regras
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
