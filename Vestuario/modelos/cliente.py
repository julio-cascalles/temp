from pydantic import BaseModel, field_validator
from modelos.util.mongo_table import MongoTable
from modelos.util.categorias import Categoria
from modelos.util.midias import Midia


class Cliente(BaseModel, MongoTable):
    nome: str
    email: str
    preferencias: list[Categoria] | str = ''
    redes_sociais: list[Midia] | str = ''

    @field_validator('preferencias')
    def valida_preferencias(lista_catego: list | str):
        if isinstance(lista_catego, str):
            lista_catego = list( Categoria.combo(lista_catego) )
        return lista_catego

    @field_validator('redes_sociais')
    def valida_redes_sociais(redes: list[Midia] | str):
        if isinstance(redes, str):
            redes = list( Midia.combo(redes) )
        return redes
