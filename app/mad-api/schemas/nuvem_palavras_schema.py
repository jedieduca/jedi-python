from typing import Optional, List, Dict
from pydantic import BaseModel, ConfigDict
from datetime import date
from decimal import Decimal

class PerguntaBaseSchema(BaseModel):
        
    id: Optional[int] = None
    id_tema: int
    pergunta: str
    respcerta: str
    resp2: Optional[str]
    resp3: Optional[str]
    resp4: Optional[str]
    caminhoimagem: str
    tempo_leitura_adulto: int
    tempo_leitura_infantil: int
    numero_palavras: int
    numero_caracteres: int

    # Necessário para o Pydantic ler objetos do SQLAlchemy
    model_config = ConfigDict(from_attributes=True)

class NuvemFilterSchema(BaseModel):
        
    categoria: Optional[str] = None
    respcerta: Optional[str] = None

class NuvemItemSchema(BaseModel):
    id: int
    pergunta: str
    respcerta: str
    categoria: str

class NuvemPalavraSchema(BaseModel):
    # Define que a resposta será uma lista de perguntas
    total_registros: int
    dados: List[NuvemItemSchema]
    texto_completo: str
    link_grafico: Dict[str, str]