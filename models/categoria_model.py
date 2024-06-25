from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Categoria:
    id: Optional[int] = None
    nome: Optional[str] = None
    descricao: Optional[str] = None