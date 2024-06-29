from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Tarefa:
    id: Optional[int] = None
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    data_vencimento: Optional[str] = None
    id_categoria: Optional[int] = None
    id_cliente: Optional[int] = None