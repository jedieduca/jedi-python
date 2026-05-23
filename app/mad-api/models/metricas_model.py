from sqlalchemy import Column, Integer, String, Boolean
from core.configs import settings
from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column

class MetricasModel(settings.DBBaseModelJEDi):
    __tablename__ = 'metricas'

    id = Column(Integer, primary_key=True)
    texto = Column(String(350))
    perguntas_tecnicas = Column(Boolean, default=False)
    possui_img = Column(Boolean, default=False)
