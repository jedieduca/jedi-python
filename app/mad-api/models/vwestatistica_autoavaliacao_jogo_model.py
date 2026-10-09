from sqlalchemy import Column, Integer, String, Numeric
from core.configs import settings
from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column

class VwEstatisticaAutoavaliacaoJogoModel(settings.DBBaseModelJEDi):
    __tablename__ = 'vw_estatistica_autoavaliacao_jogo'

    id = Column(Integer, primary_key=True)
    escola = Column(String(150))
    turma = Column(String(50))
    ordem_auto = Column(Integer)
    autoavaliacao = Column(String(20))
    ordem_jogo = Column(Integer)
    avaliacao_jogo = Column(String(20))
    qtd = Column(Integer)
    total_grupo: Mapped[Decimal] = mapped_column(Numeric(precision=32, scale=0))
    pct_no_grupo: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=1))
