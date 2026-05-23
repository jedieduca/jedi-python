import time 
from fastapi import APIRouter, status, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from models.usuario_model import UsuarioModel
from repositories.regras_repository import RegrasRepository
from services.regras import RegrasService
from schemas.vwapriori_schema import RespostaApriorSchema
from core.deps import get_session_JEDi, get_current_user
from core.configs import settings

router = APIRouter(redirect_slashes=False)

# GET Regras
@router.get('', status_code=status.HTTP_200_OK, response_model=RespostaApriorSchema)
async def get_rules(request: Request, usuario_logado: UsuarioModel = Depends(get_current_user), db: AsyncSession = Depends(get_session_JEDi)):
    try:
        # Instancia o repositório passando a sessão do banco e a camada de serviços
        repo     = RegrasRepository(db)
        service  = RegrasService()
        
        # Chama a camada de dados de forma isolada
        data = await repo.get_dados_mineracao()
        
        regras, links_imagens = await service.processar_regras_associacao(data)

        if not regras:
            raise HTTPException(
                detail='Nenhuma regra encontrada para os parâmetros atuais...', 
                status_code=status.HTTP_404_NOT_FOUND
            )

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
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
