from enum import Enum
from pydantic import BaseModel, field_validator
from modelos.util.mongo_table import MongoTable
from modelos.util.categorias import Categoria
from modelos.util.midias import Midia


class TipoCampanha(Enum):
    LANCAMENTO = 'Lançamento'
    DESCONTO = 'Desconto'
    PROSPECCAO = 'Prospecção'


class Campanha(BaseModel, MongoTable):
    nome: str
    tipo: TipoCampanha
    ativa:bool
    categorias: list[Categoria] | str = ''
    midias: list[Midia] | str = ''

    @field_validator('categorias')
    def valida_categorias(lista_catego: list | str):
        if isinstance(lista_catego, str):
            lista_catego = list( Categoria.combo(lista_catego) )
        return lista_catego

    @field_validator('midias')
    def valida_midias(redes: list[Midia] | str):
        if isinstance(redes, str):
            redes = list( Midia.combo(redes) )
        return redes
