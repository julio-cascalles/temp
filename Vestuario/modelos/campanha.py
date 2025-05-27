from datetime import datetime, timedelta
from pydantic import BaseModel, field_validator
from modelos.util.mongo_table import MongoTable
from modelos.util.categorias import Categoria
from modelos.util.midias import Midia
from modelos.produto import Produto, Cupom
from modelos.cliente import Cliente


class Campanha(BaseModel):
    nome: str
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
    
    @classmethod
    def find_all(cls, **args) -> list:
        result = []
        for sub in cls.__subclasses__():
            result += sub.find(**args)
        return result


class Lancamento(Campanha, MongoTable):
    produtos: list[Produto| dict]

    def save(self):
        gravados = []
        for produto in self.produtos:
            if Produto.find(nome=produto.nome):
                continue # --- ignora duplicado
            if not produto.categoria:
                produto.categoria = self.categorias.copy()
            gravados.append(produto.model_dump())
            produto.save()
        self.produtos = gravados
        if not gravados:
            return False
        super().save()
        return True


class Liquidacao(Campanha, MongoTable):
    desconto: float

    @field_validator('desconto')
    def valida_desconto(novo_desconto: float):
        if 0.7 > novo_desconto >= 0.01:
            return novo_desconto
        raise ValueError("""
            O desconto deve estar entre
             0.01 (1%)  e  0.7 (70%)
        """)

    def save(self):
        encontrados = Produto.find(
            categoria={'$in': self.categorias}
        )
        if not encontrados:
            return False
        data_limite = datetime.today() + timedelta(days=15)
        cupom = Cupom(
            desconto=self.desconto,
            valido_ate=data_limite.strftime('%Y-%m-%d')
        ).model_dump()
        for produto in encontrados:
            produto.cupom = cupom
            produto.save()
        super().save()
        return True


class Prospeccao(Campanha, MongoTable):
    clientes: list[Cliente | dict]

    def save(self):
        gravados = []
        for cliente in self.clientes:
            if Cliente.find(nome=cliente.nome):
                continue # -- ignora os duplicados
            if not cliente.redes_sociais:
                cliente.redes_sociais = self.midias.copy()
            if not cliente.preferencias:
                cliente.preferencias = self.categorias.copy()
            gravados.append(cliente.model_dump())
            cliente.save()
        self.clientes = gravados
        if not gravados:
            return False
        super().save()
        return True
