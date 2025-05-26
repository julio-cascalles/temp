from pydantic import BaseModel, field_validator
from datetime import datetime
from modelos.util.mongo_table import MongoTable
from modelos.util.categorias import Categoria


class Cupom(BaseModel, MongoTable):
    desconto: float
    valido_ate: datetime


class Produto(BaseModel, MongoTable):
    """
    Apesar de chamar `Produto`, esta entidade
    está relacionada à LINHA de produtos, portanto
    NÃO tem campos como tamanho, cor...que seriam
    atributos de itens individuais.
    """
    nome: str
    categoria: list[Categoria] | str = ''
    valor: float
    cupom: Cupom = None

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

    @property
    def total(self) -> float:
        preco_normal = (
            not self.cupom
            or
            self.cupom.valido_ate < datetime.today()
        )
        if preco_normal:
            self.cupom = None
            return self.valor
        return self.valor * (1 - self.cupom.desconto)
