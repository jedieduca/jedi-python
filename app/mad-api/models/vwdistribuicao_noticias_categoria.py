from sqlalchemy import Column, Integer, String, Numeric
from core.configs import settings
from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column

class VwDistribuicaoNoticiasCategoriaModel(settings.DBBaseModelJEDi):
    __tablename__ = 'vw_distribuicao_noticias_categoria'

    id = Column(Integer, primary_key=True)
    categoria = Column(String(150))
    fake_qt = Column(Integer)
    fake_perc: Mapped[Decimal] = mapped_column(Numeric(precision=26, scale=2))
    nao_fake_qt = Column(Integer)
    nao_fake_perc: Mapped[Decimal] = mapped_column(Numeric(precision=26, scale=2))