from sqlalchemy import Column, Integer, String
from core.configs import settings

class VwAnaliseIdadeModel(settings.DBBaseModelJEDi):
    __tablename__ = 'vw_analise_idade'

    id = Column(Integer, primary_key=True)
    escola = Column(String(150))
    turma = Column(String(50))
    id_jogador = Column(Integer)
    idade = Column(Integer)
