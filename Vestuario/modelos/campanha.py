from enum import Enum
from pydantic import BaseModel
from modelos.util.mongo_table import MongoTable
from modelos.util.subcategorias import SubCategoria
from modelos.util.midias import Midia


class TipoCampanha(Enum):
    LANCAMENTO = 'Lançamento'
    DESCONTO = 'Desconto'
    PROSPECCAO = 'Prospecção'


class Campanha(BaseModel, MongoTable):
    nome: str
    tipo: TipoCampanha
    ativa:bool
    categorias: list[SubCategoria]
    midias: list[Midia]
