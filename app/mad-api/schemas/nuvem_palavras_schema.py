from typing import Optional, List, Dict
from pydantic import BaseModel, ConfigDict
from datetime import date
from decimal import Decimal

class PerguntaBaseSchema(BaseModel):
        
    id: Optional[int] = None
    id_tema: int
    pergunta: str
    resp_certa: Optional[str] = None
    resp_2: Optional[str]
    resp_3: Optional[str]
    resp_4: Optional[str]
    caminho_imagem: str
    tempo_leitura_adulto: int
    tempo_leitura_infantil: int
    numero_palavras: int
    numero_caracteres: int

    # Necessário para o Pydantic ler objetos do SQLAlchemy
    model_config = ConfigDict(from_attributes=True)

class NuvemFilterSchema(BaseModel):
        
    categoria: Optional[str] = None
    resp_certa: Optional[str] = None

class NuvemItemSchema(BaseModel):
    id: int
    pergunta: str
    resp_certa: Optional[str] = None
    categoria: str

class NuvemPalavraSchema(BaseModel):
    # Define que a resposta será uma lista de perguntas
    total_registros: int
    dados: List[NuvemItemSchema]
    texto_completo: str
    link_grafico: Dict[str, str]