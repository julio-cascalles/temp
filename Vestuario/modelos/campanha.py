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
    def find(cls, **args) -> list:
        result = []
        for sub in cls.__subclasses__():
            result += sub.find(**args)
        return result


class Lancamento(Campanha, MongoTable):
    produtos: list[Produto]

    def save(self):
        """
        Faz o lançamento dos novos produtos,
        deixando-os disponíveis para consumo:
        """
        for produto in self.produtos:
            if Produto.find(nome=produto.nome):
                continue # --- ignora duplicado
            if not produto.categoria:
                produto.categoria = self.categorias.copy()
            produto.save()
        super().save()


class Liquidacao(Campanha, MongoTable):
    desconto: float

    def save(self):
        """
        Aplica cupom de desconto em
        todos os produtos da campanha
        """
        cupom = Cupom(
            desconto=self.desconto,
            valido_ate=datetime.today() + timedelta(days=15)
        )
        produto: Produto
        for produto in self.produtos:
            produto.cupom = cupom
            produto.save()
        super().save()


class Prospeccao(Campanha, MongoTable):
    clientes: list[Cliente]

    def save(self):
        """
        Converte `leads` em clientes
        """
        for cliente in self.clientes:
            if Cliente.find(nome=cliente.nome):
                continue # -- ignora os duplicados
            if not cliente.redes_sociais:
                cliente.redes_sociais = self.midias.copy()
            if not cliente.preferencias:
                cliente.preferencias = self.categorias.copy()
            cliente.save()
        super().save()
