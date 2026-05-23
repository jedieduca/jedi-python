from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from core.configs import settings


class PerguntasModel(settings.DBBaseModelJEDi):
    __tablename__ = 'pergunta2'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_tema = Column(Integer, ForeignKey("tema2.id"), nullable=False)
    pergunta = Column(Text, nullable=False)
    respcerta = Column(Text, nullable=False)
    resp2 = Column(Text)
    resp3 = Column(Text)
    resp4 = Column(Text)
    caminhoimagem = Column(String(50))
    tempo_leitura_adulto = Column(Integer, default=0)
    tempo_leitura_infantil = Column(Integer, default=0)
    numero_palavras = Column(Integer)
    numero_caracteres = Column(Integer)

    # Relacionamentos
    categorias_vinculadas = relationship("PerguntasCategoriasModel", back_populates="pergunta")
