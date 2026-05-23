from sqlalchemy import Column, Integer, String, Numeric
from core.configs import settings
from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column

class VwEstatisticaCategoriaTurmaModel(settings.DBBaseModelJEDi):
    __tablename__ = 'vw_estatistica_categoria_turma'

    id = Column(Integer, primary_key=True)
    escola = Column(String(150))
    turma = Column(String(50))
    categoria = Column(String(30))
    media_acertos: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=2))
    media_erros: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=2))