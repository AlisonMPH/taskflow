from pydantic import BaseModel, field_validator
from datetime import date

from util.validators import *

class NovaTarefaDTO(BaseModel):
    titulo: str
    descricao: str
    data_vencimento: date
    id_categoria: int

    @field_validator("data_vencimento")
    def validar_data_nascimento(cls, v):
        msg = is_not_empty(v, "Data de Vencimento")
        if not msg:
            msg = is_date_valid(v, "Data de Vencimento")
        if msg:
            raise ValueError(msg)
        return v

    @field_validator("descricao")
    def validar_endereco(cls, v):
        msg = is_size_between(v, "Descrição: ", 8, 128)
        if msg:
            raise ValueError(msg)
        return v