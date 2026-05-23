from typing import Optional, List, Dict
from pydantic import BaseModel
from datetime import date
from decimal import Decimal

class VwAprioriSchema(BaseModel):
        
    id: Optional[int] = None
    origem: str
    escola: str
    turma: str
    login: str
    jogador: str
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

# Representa o objeto de retorno final da rota
class RespostaApriorSchema(BaseModel):
    total_regras: int
    links_imagens: Dict[str, str]
    regras: List[RegrasAssociacaoSchema]