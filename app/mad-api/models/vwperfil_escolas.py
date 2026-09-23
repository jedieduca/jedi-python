from sqlalchemy import Column, Integer, String, Numeric
from core.configs import settings
from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column

class VwPerfilEscolasModel(settings.DBBaseModelJEDi):
    __tablename__ = 'vw_perfil_escolas'

    id = Column(Integer, primary_key=True)
    escola = Column(String(150))
    num_turmas: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=0))
    num_discentes: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=0))
    num_docentes: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=0))
    num_gestores: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=0))
    num_secretarios: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=0))
    total: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=0))
