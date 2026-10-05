from typing import Optional, List, Dict, Literal
from pydantic import BaseModel
from datetime import date
from decimal import Decimal

class VwAprioriSchema(BaseModel):
        
    id: Optional[int] = None
    escola: str
    turma: str
    login: str
    nome: str
    dt_jogo: date
    idade: int
    auto_avaliacao: str
    avaliacao_jogo: str
    tutor: int
    categoria: str
    tema: str
    numero_partidas: int
    tempo_gasto: Decimal
    percentual_acertos: Decimal
    percentual_erros: Decimal
    capacidade_critica: str

class RegrasAssociacaoSchema(BaseModel):
    antecedents: List[str]
    consequents: List[str]
    support: float
    confidence: float
    lift: float

class RegrasAssociacaorFilterSchema(BaseModel):

    escola: Optional[str] = None
    turma: Optional[str] = None
    nome: Optional[str] = None
    capacidade_critica: Optional[str] = None
    # Filtros aplicados sobre as regras mineradas, antes da geração dos gráficos
    antecedente: Optional[str] = None
    consequente: Optional[str] = None
    suporte_min: Optional[float] = None
    confianca_min: Optional[float] = None
    lift_min: Optional[float] = None

# Representa o objeto de retorno final da rota
class RespostaApriorSchema(BaseModel):
    total_regras: int
    links_imagens: Dict[str, str]
    regras: List[RegrasAssociacaoSchema]
    nivel: Literal["sucesso", "info", "warning"] = "sucesso"
    mensagem: Optional[str] = None