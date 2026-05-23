from sqlalchemy import Column, Integer, String, Date, Numeric
from core.configs import settings
from datetime import date
from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column

class VwAprioriModel(settings.DBBaseModelJEDi):
    __tablename__ = 'vw_apriori'

    id = Column(Integer, primary_key=True)
    escola = Column(String(150))
    turma = Column(String(15))
    login = Column(String(12))
    jogador = Column(String(12))
    dt_jogo: Mapped[date] = mapped_column(Date)
    idade = Column(Integer)
    auto_avaliacao = Column(String(14))
    avaliacao_jogo = Column(String(14))
    tutor = Column(Integer)
    categoria = Column(String(30))
    tema = Column(String(50))
    numero_partidas = Column(Integer)
    tempo_gasto: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=2))
    percentual_acertos: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=2))
    percentual_erros: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=2))
    capacidade_critica = Column(String(8))
