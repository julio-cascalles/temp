from pydantic import BaseModel
from datetime import datetime
from typing import Union
from modelos.util.subcategorias import SubCategoria
from modelos.util.midias import Midia


class Cliente(BaseModel):
    nome: str
    ultima_compra: Union[str, datetime] = ''
    preferencias: list[SubCategoria]
    email: str
    redes_sociais: dict[Midia, str]
