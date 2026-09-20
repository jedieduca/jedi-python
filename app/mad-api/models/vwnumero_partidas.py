from sqlalchemy import Column, Integer, String, Numeric
from core.configs import settings
from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column

class VwNumeroPartidasModel(settings.DBBaseModelJEDi):
    __tablename__ = 'vw_numero_partidas'

    id = Column(Integer, primary_key=True)
    usuario = Column(String(150))
    grupo = Column(String(150))
    escola = Column(String(150))
    turma = Column(String(50))
    aluno = Column(String(150))
    dt_jogo = Column(String(150)) 
    numero_partidas: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=0))
