from typing import Optional, List, Dict, Any, Union, Literal
from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field
from decimal import Decimal
from datetime import date

class EstisticaAvaliacaoSchema(BaseModel):
        
    id: Optional[int] = None
    escola: Optional[str]
    turma: Optional[str]
    tipo_avaliacao: str
    nota: str
    qtd: int

class EstisticaAvaliacaoFilterSchema(BaseModel):
        
    id: Optional[int] = None
    escola: Optional[str] = None
    # Lista: aceita ?turma=A&turma=B (professor com várias turmas); Query() faz o FastAPI ler da URL
    turma: Optional[List[str]] = Field(Query(None))

class EstatisticaCategoriaTurmaSchema(BaseModel):

    id: Optional[int] = None
    escola: Optional[str]
    turma: str
    categoria: str
    media_acertos: Decimal
    media_erros: Decimal

class EstisticaCategoriaFilterSchema(BaseModel):
        
    id: Optional[int] = None
    escola: Optional[str] = None
    # Lista: aceita ?turma=A&turma=B (professor com várias turmas); Query() faz o FastAPI ler da URL
    turma: Optional[List[str]] = Field(Query(None))
    categoria: Optional[str] = None

class EstatisticaPartidaTurmaSchema(BaseModel):

    id: Optional[int] = None
    escola: str
    turma: str
    PI: Decimal
    PF: Decimal

class EstatisticaPartidaFilterSchema(BaseModel):

    id: Optional[int] = None
    escola: Optional[str] = None
    # Lista: aceita ?turma=A&turma=B (professor com várias turmas); Query() faz o FastAPI ler da URL
    turma: Optional[List[str]] = Field(Query(None))
 
class DistribuicaoNotociaCategoriaSchema(BaseModel):

    id: Optional[int] = None
    categoria: str
    fake_qt: int
    fake_perc: Decimal
    nao_fake_qt: int
    nao_fake_perc: Decimal

class DistribuicaoNotociaCategoriaFilterSchema(BaseModel):

    id: Optional[int] = None
    categoria: Optional[str] = None

class RankingPartidasSchema(BaseModel):

    id: Optional[int] = None
    escola: Optional[str] = None
    turma: Optional[str] = None
    aluno: Optional[str] = None
    dt_jogo: Optional[str] = None
    numero_partidas: Decimal

class RankingMatchesFilterSchema(BaseModel):

    id: Optional[int] = None
    escola: Optional[str] = None
    # Lista: aceita ?turma=A&turma=B (professor com várias turmas); Query() faz o FastAPI ler da URL
    turma: Optional[List[str]] = Field(Query(None))
    dt_jogo_ini: Optional[date] = None
    dt_jogo_fim: Optional[date] = None

class PerfilEscolaSchema(BaseModel):
    id: Optional[int] = None
    escola: str
    num_turmas: int
    num_discentes: int
    num_docentes: int
    num_gestores: int
    num_secretarios: int
    total: int

class PerfilEscolaFilterSchema(BaseModel):
    id: Optional[int] = None
    escola: Optional[str] = None

class CapacidadeCriticaSchema(BaseModel):
    id: Optional[int] = None
    escola: Optional[str]
    turma: Optional[str]
    capacidade_critica: str

class CapacidadeCriticaFilterSchema(BaseModel):
    id: Optional[int] = None
    escola: Optional[str] = None
    # Lista: aceita ?turma=A&turma=B (professor com várias turmas); Query() faz o FastAPI ler da URL
    turma: Optional[List[str]] = Field(Query(None))
    dt_jogo_ini: Optional[date] = None
    dt_jogo_fim: Optional[date] = None
    capacidade_critica: Optional[str] = None

class AnaliseIdadeSchema(BaseModel):
    id: Optional[int] = None
    escola: Optional[str]
    turma: Optional[str]
    id_jogador: int
    idade: Optional[int]

class AnaliseIdadeFilterSchema(BaseModel):
    id: Optional[int] = None
    escola: Optional[str] = None
    # Lista: aceita ?turma=A&turma=B (professor com várias turmas); Query() faz o FastAPI ler da URL
    turma: Optional[List[str]] = Field(Query(None))

class AutoavaliacaoJogoSchema(BaseModel):
    id: Optional[int] = None
    escola: Optional[str]
    turma: Optional[str]
    ordem_auto: int
    autoavaliacao: str
    ordem_jogo: int
    avaliacao_jogo: str
    qtd: int
    total_grupo: int
    pct_no_grupo: Optional[Decimal] = None   # NULL quando ninguém se autoavaliou no nível

class AutoavaliacaoJogoFilterSchema(BaseModel):
    id: Optional[int] = None
    escola: Optional[str] = None
    # Lista: aceita ?turma=A&turma=B (professor com várias turmas); Query() faz o FastAPI ler da URL
    turma: Optional[List[str]] = Field(Query(None))

class RespostaEstatisticaSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    total: int
    link_imagem: Dict[str, str]
    dados: List[Union[
        EstisticaAvaliacaoSchema, 
        EstatisticaCategoriaTurmaSchema, 
        EstatisticaPartidaTurmaSchema, 
        DistribuicaoNotociaCategoriaSchema,
        AnaliseIdadeSchema,
        RankingPartidasSchema,
        PerfilEscolaSchema,
        CapacidadeCriticaSchema,
        AutoavaliacaoJogoSchema,
    ]]
    nivel: Literal["sucesso", "info", "warning"] = "sucesso"
    mensagem: Optional[str] = None
