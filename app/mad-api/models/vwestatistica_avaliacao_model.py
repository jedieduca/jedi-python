from sqlalchemy import Column, Integer, String, Numeric
from core.configs import settings
from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column

class VwEstatisticaAvaliacoesModel(settings.DBBaseModelJEDi):
    __tablename__ = 'vw_estatistica_avaliacoes'

    id = Column(Integer, primary_key=True)
    escola = Column(String(150))
    turma = Column(String(50))
    avaliacao = Column(String(14))
    autoavaliacao: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=2))
    avaliacao_jogo: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=2))

