from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from core.configs import settings


class CategoriaModel(settings.DBBaseModelJEDi):
    __tablename__ = 'categoria'

    id = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String(255), nullable=False)

    # Relacionamento com a tabela associativa
    perguntas_vinculadas = relationship("PerguntasCategoriasModel", back_populates="categoria")
