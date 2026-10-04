from sqlalchemy import Column, Integer, String
from core.configs import settings

class VwEstatisticaAvaliacoesModel(settings.DBBaseModelJEDi):
    __tablename__ = 'vw_estatistica_avaliacoes'

    id = Column(Integer, primary_key=True)
    escola = Column(String(150))
    turma = Column(String(50))
    tipo_avaliacao = Column(String(20))
    nota = Column(String(50))
    qtd = Column(Integer)

