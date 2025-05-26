from pydantic import BaseModel, field_validator
from datetime import datetime
from modelos.util.mongo_table import MongoTable
from modelos.util.categorias import Categoria


class Cupom(BaseModel):
    desconto: float
    valido_ate: str  # -- Data em formato '2024-12-25'

    @staticmethod
    def dentro_prazo(dt_exp: str) -> bool:
        dt_exp = datetime.strptime(dt_exp, '%Y-%m-%d')
        return datetime.today() <= dt_exp

    @field_validator('valido_ate')
    def valida_validade(data_limite: str):
        if not Cupom.dentro_prazo(data_limite):
            ValueError('A data deve ser até hoje.')
        return data_limite

    def expirou(self) -> bool:
        return not self.dentro_prazo(self.valido_ate)


class Produto(BaseModel, MongoTable):
    nome: str
    categoria: list[Categoria] | str = ''
    valor: float
    cupom: dict | None = None

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
