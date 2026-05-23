from typing import Optional, Any
from pydantic import BaseModel
from decimal import Decimal

class MetricasSchemaBase(BaseModel):

    id: Optional[int] = None
    texto: str
    perguntas_tecnicas: bool = False
    possui_img: bool = False

class RespostaMetricasSchema(BaseModel):

    texto: str
    numero_palavras: int
    numero_caracteres: int
    publico_infantil: Decimal
    publico_adulto: Decimal

