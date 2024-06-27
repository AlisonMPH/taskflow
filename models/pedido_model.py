from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from models.cliente_model import Cliente


@dataclass
class Pedido:
    id: Optional[int] = None
    data_hora: Optional[datetime] = None
    valor_total: Optional[float] = None
    endereco_entrega: Optional[str] = None
    estado: Optional[str] = None
    id_cliente: Optional[int] = None
