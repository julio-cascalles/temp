class CaixaEletronico(list):
    VALORES_POSSIVEIS = (50, 20, 10, 5, 2, 1)
    
    def append(self, valor: int):
        if valor not in self.VALORES_POSSIVEIS:
            raise ValueError(f'A nota de {valor} NÃO existe!')
        return super().append(valor)
    
    def deposito(self, notas: list):
        for valor in notas:
            self.append(valor)
    
    def __init__(self, notas: list=None):
        if notas: self.deposito(notas)

    def pop(self, valor: int) -> int:
        i = self.index(valor)
        return super().pop(i)

    def saque(self, valor: int) -> dict:
        entrega = {}
        while valor:
            cedula = max(
                nota for nota in self.VALORES_POSSIVEIS 
                if nota <= valor and nota in self
            )
            valor -= self.pop(cedula)
            entrega[cedula] = entrega.get(cedula, 0) + 1
        return entrega


if __name__ == '__main__':
    caixa = CaixaEletronico(
        [50]*21 + [20]*52 + [10]*101 + [5]*201 + [2]*500 + [1]*1000
    )   # . . .  sum(caixa) == sum(range(1, 111)) == 6105
    #                                     ^
    #                                     |    
    for i in range(1, 111): # ------------+
        assert i == sum( nota * qtd for nota, qtd in caixa.saque(i).items() )
    assert caixa == []
    permite_valor_invalido = True
    try:
        caixa.append(3)
    except:
        permite_valor_invalido = False
    assert not permite_valor_invalido
    print('Passou em todos os testes!!'.center(50, '*'))
