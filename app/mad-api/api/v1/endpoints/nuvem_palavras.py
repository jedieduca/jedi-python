import time
from fastapi import APIRouter, status, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

'''
import nltk
from nltk.corpus import stopwords
'''
from models.usuario_model import UsuarioModel
from repositories.nuvem_palavras_repository import NuvemPalavrasRepository
from schemas.nuvem_palavras_schema import (
    NuvemFilterSchema,
    NuvemPalavraSchema
)
from services.nuvem_palavras import NuvemPalavarasService

from core.deps import get_session_JEDi, get_current_user
from core.configs import settings

router = APIRouter(redirect_slashes=False)

# GET Regras
@router.get('', status_code=status.HTTP_200_OK, response_model=NuvemPalavraSchema)
async def get_palavras(
    request: Request,
    filters: NuvemFilterSchema = Depends(),
    usuario_logado: UsuarioModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_session_JEDi)
):
    try:
        # 1. Busca os dados via Repositório
        repo = NuvemPalavrasRepository(db)
        
         # Chama a camada de dados de forma isolada
        registros = await repo.get_perguntas_para_nuvem(filters)
        
        if not registros:
            raise HTTPException(detail='Não foi possível gerar os dados.', status_code=status.HTTP_404_NOT_FOUND)
        
        # 2. Processa a lógica via Serviço
        service = NuvemPalavarasService()
        path_relativo = "static/estatisticas/img/nuvem_questoes.jpg"
        texto_original = await service.processar_texto_e_gerar_nuvem(registros, path_relativo)

        '''
        # Baixar a lista de stopwords do NLTK
        nltk.download('stopwords')
        stop_words_pt = set(stopwords.words('portuguese'))
        
        # Configurando Stopwords em Português
        palavras_extras = {"de", "a", "o", "que", "e", "do", "da", "em", "um", "para", "é", "com", "na", "no", "os", "as", "ao", "se", "sobre", "diz", "faz", "deve", "pode"}
        # Você pode somar as stopwords padrão da biblioteca se desejar
        stop_words_pt.update(palavras_extras)        
        '''
        base_url = settings.URL_BASE
        timestamp = int(time.time())
        link = {
            "link": f"{base_url}/{path_relativo}?v={timestamp}"
        }

        return {
            "total_registros": len(registros),
            "dados": registros,
            "texto_completo": texto_original,
            "link_grafico": link 
        }
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        
