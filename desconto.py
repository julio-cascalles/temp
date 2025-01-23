from dataclasses import dataclass
from datetime import datetime

HOJE = datetime.today()


@dataclass
class Cliente:
    nome: str
    nascimento: datetime
    fidelidade: bool = False

    @property
    def idade(self) -> int:
        nasc = self.nascimento
        return HOJE.year - nasc.year - (
            (HOJE.month, HOJE.day) < (nasc.month, nasc.day)
        )

    def aniversário(self) -> bool:
        nasc = self.nascimento
        return all([
            HOJE.day == nasc.day,
            HOJE.month == nasc.month
        ])


@dataclass
class Produto:
    nome: str
    valor: float
    em_promoção: bool = False


@dataclass
class Compra:
    cliente: Cliente
    produto: Produto
    quantidade: int


REGRAS_BASICAS = {
    'desconto para idosos': (
        lambda compra: 10 if compra.cliente.idade > 65 else 0 
    ),'programa de fidelidade': (
        lambda compra: 5 if compra.cliente.fidelidade else 0 
    ),'presente de aniversário': (
        lambda compra: 15  if compra.cliente.aniversário() else 0
    ),'promoção do produto': (
        lambda compra: 20 if compra.produto.em_promoção else 0 
    ),'desconto por quantidade': (
        lambda compra: 7 if compra.quantidade > 5 else 0 
    ),}

def calcula_desconto(compra: Compra, regras: dict=REGRAS_BASICAS) -> float:
    total = compra.produto.valor * compra.quantidade
    preço_original = True
    for nome_regra, func_percentual in regras.items():
        desconto = func_percentual(compra)
        if desconto:
            print('Aplicando "{}" ({}%) em {} para {}.'.format(
                nome_regra, desconto, compra.produto.nome, compra.cliente.nome
            ))
            total *= (1 - desconto / 100)
            preço_original = False
    if preço_original:
        print(f'Nenhum desconto para {compra.cliente.nome} :((')
    return total


if __name__ == "__main__":
    seu_Jolêno = Cliente('Joleno Dos Bitus', datetime(1945, 8, 13))
    compra_do_seu_Jolêno = [
        Compra(produto=Produto('Xampu', 7.14), 
            quantidade=3,   cliente=seu_Jolêno),
        Compra(produto=Produto('Sabonete', 3.5),
            quantidade=12,  cliente=seu_Jolêno),
        Compra(produto=Produto('Desodorante', 11.14, em_promoção=True),
            quantidade=1,   cliente=seu_Jolêno)
    ]
    compras_da_Paula = [
        Compra(produto=Produto('Queijo emental', valor=80.13),
            quantidade=1, cliente=Cliente('Paula Tejano', fidelidade=True,
                nascimento=datetime(2000, HOJE.month, HOJE.day) # ---- simula uma cliente fazendo aniversário hoje
        ))
    ]
    for compra in compra_do_seu_Jolêno + compras_da_Paula:
        print('-'*50, 'Preço final: {:.2f}'.format(calcula_desconto(compra)))
