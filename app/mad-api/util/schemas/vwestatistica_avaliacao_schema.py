from typing import Optional, List, Dict
from pydantic import BaseModel
from decimal import Decimal

class VwEstisticaAvaliacaoSchema(BaseModel):
        
    id: Optional[int] = None
    avaliacao: str
    autoavaliacao: Decimal
    avaliacao_jogo: Decimal