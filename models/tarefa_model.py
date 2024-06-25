from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Tarefa:
    id: Optional[int] = None
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    data_vencimento: Optional[date] = None
    id_categoria: Optional[str] = None
    id_cliente: Optional[str] = None