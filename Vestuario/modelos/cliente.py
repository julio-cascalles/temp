from pydantic import BaseModel
from modelos.util.mongo_table import MongoTable
from modelos.util.subcategorias import SubCategoria
from modelos.util.midias import Midia


class Cliente(BaseModel, MongoTable):
    nome: str
    preferencias: list[SubCategoria]
    email: str
    redes_sociais: dict[Midia, str]
