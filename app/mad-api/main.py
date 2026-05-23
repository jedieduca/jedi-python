import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from core.configs import settings
from api.v1.api import api_router

# 🔹 CORRIGIDO: Define o caminho absoluto interno do container para evitar conflitos com volumes
BASE_STATIC_DIR = "/app/mad-api/static"

# Criar subpastas necessárias se não existirem dentro do diretório correto
os.makedirs(os.path.join(BASE_STATIC_DIR, "regras/img"), exist_ok=True)
os.makedirs(os.path.join(BASE_STATIC_DIR, "estatisticas/img"), exist_ok=True)
os.makedirs(os.path.join(BASE_STATIC_DIR, "nuvem_palavaras/img"), exist_ok=True)

app = FastAPI(
    title='JEDi Educa - API para Mineração de Dados',
    version='0.0.1',
    description='Uma API inteligente para análise de dados oriundos do JEDI Educa.',
    # 🔹 DESCOMENTADO E ATIVADO: Essencial para o NGINX rotear o /api/docs sem dar 404
    root_path="/api"
)

app.include_router(api_router, prefix=settings.API_V1_STR)

# 🔹 CORRIGIDO COM PRIORIDADE: Mapeia a rota HTTP '/static' para a pasta absoluta compartilhada com o volume
app.mount("/static", StaticFiles(directory=BASE_STATIC_DIR), name="static")

if __name__ == '__main__':
    import uvicorn
    # 🔹 CORRIGIDO: Host alterado para 0.0.0.0 (visível na rede Docker) e porta alinhada com o Compose (8001)
    uvicorn.run("main:app", host="0.0.0.0", port=8001, log_level="debug", reload=True)