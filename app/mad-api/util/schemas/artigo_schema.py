from typing import Optional
from pydantic import ConfigDict, BaseModel, HttpUrl

class ArtigoSchema(BaseModel):
    id: Optional[int] = None
    titulo: str
    descricao: str
    url_fonte: HttpUrl
    usuario_id: Optional[int] = None

    # class Config:
    #     orm_mode = True

    model_config = ConfigDict(from_attributes=True)
