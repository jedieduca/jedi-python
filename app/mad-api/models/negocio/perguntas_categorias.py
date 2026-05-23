from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from core.configs import settings


class PerguntasCategoriasModel(settings.DBBaseModelJEDi):
    __tablename__ = 'pergunta_categoria2'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_tema = Column(Integer, ForeignKey("tema2.id"))
    id_pergunta = Column(Integer, ForeignKey("pergunta2.id"))
    id_categoria = Column(Integer, ForeignKey("categoria.id"))

    # Relacionamentos para facilitar o acesso via código
    pergunta  = relationship("PerguntasModel", back_populates="categorias_vinculadas")
    categoria = relationship("CategoriaModel", back_populates="perguntas_vinculadas")
