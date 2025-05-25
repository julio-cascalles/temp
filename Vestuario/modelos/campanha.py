from enum import Enum
from pydantic import BaseModel
from modelos.util.subcategorias import SubCategoria
from modelos.util.midias import Midia


class TipoCampanha(Enum):
    LANCAMENTO = 'Lançamento'
    DESCONTO = 'Desconto'
    ANUNCIO = 'Anúncio'


class Campanha(BaseModel):
    nome: str
    tipo: TipoCampanha
    ativa:bool
    categorias: list[SubCategoria]
    midias: list[Midia]
