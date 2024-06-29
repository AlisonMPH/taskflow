from datetime import date
from pydantic import BaseModel, field_validator
from util.validators import is_date_future, is_not_empty, is_size_between

class NovaTarefaDTO(BaseModel):
    titulo: str
    descricao: str
    data_vencimento: date
    id_categoria: str

    @field_validator("titulo")
    def validar_titulo(cls, v):
        msg = is_size_between(v, "Titulo", 4, 20)
        if msg:
            raise ValueError(msg)
        return v

    @field_validator("descricao")
    def validar_descricao(cls, v):
        msg = is_size_between(v, "Descrição", 8, 128)
        if msg:
            raise ValueError(msg)
        return v
    
    @field_validator("data_vencimento")
    def validar_data_vencimento(cls, v):
        msg = is_date_future(v, "Data de Vencimento")
        if msg:
            raise ValueError(msg)
        return v
    
    @field_validator("id_categoria")
    def validar_categoria(cls, v):
        msg = is_not_empty(v, "Categoria")
        if msg:
            raise ValueError(msg)
        return v