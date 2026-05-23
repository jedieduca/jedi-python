from sqlalchemy import Column, Integer, String, Numeric
from core.configs import settings
from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column

class VwEstatisticaPartidaTurmaModel(settings.DBBaseModelJEDi):
    __tablename__ = 'vw_estatistica_partida_turma'

    id = Column(Integer, primary_key=True)
    escola = Column(String(150))
    turma = Column(String(50))
    PI: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=2))
    PF: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=2))