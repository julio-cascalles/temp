from pydantic import BaseModel, field_validator
from modelos.util.mongo_table import MongoTable
from modelos.util.categorias import Categoria


class Produto(BaseModel, MongoTable):
    nome: str
    categoria: list[Categoria] | str
    estoque: int
    valor: float

    # tamanho: Tamanho # --- Pequeno, Medio, Grande
    # cor: Cor # --- Vermelho, Amarelo, Azul, Verde, Laranja, Roxo

    @field_validator('estoque')
    def valida_estoque(novo_estoque: int) -> int:
        if novo_estoque < 0:
            raise ValueError('O estoque não pode ser menor que zero.')
        return novo_estoque

    @field_validator('valor')
    def valida_valor(novo_valor: int) -> int:
        if novo_valor <= 0:
            raise ValueError('''
                O valor não pode ser menor ou igual a zero.
            ''')
        return novo_valor

    @field_validator('categoria')
    def valida_categorias(lista_catego: list | str):
        if isinstance(lista_catego, str):
            lista_catego = list( Categoria.combo(lista_catego) )
        return lista_catego
