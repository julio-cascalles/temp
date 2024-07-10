class Empresa:
    def __init__(self, lucro: float) -> None:
        self.lucro = lucro

class Trabalhador:
    fixo: float

    def __init__(self, empresa: Empresa):
        self.empresa = empresa

    def comissão(self) -> float:
        return 0.00
    
    def salário(self, descontos: float=0.00) -> float:
        return self.fixo + self.comissão() - descontos


class Operário(Trabalhador):
    fixo = 1_000


class Vendedor(Trabalhador):
    fixo = 2_000

    def __init__(self, empresa: Empresa):
        super().__init__(empresa)
        self.vendas = 0.00

    def comissão(self) -> float:
        return self.vendas * 0.05 # <--- 5% das vendas desse vendedor


class Diretor(Trabalhador):
    fixo = 15_000

    def comissão(self) -> float:
        return self.empresa.lucro * 0.01 # <-- 1% do lucro da empresa


if __name__ == "__main__":
    Americanas = Empresa(1e6)
    zé = Operário(Americanas)
    Enzo = Vendedor(Americanas)
    Enzo.vendas = 10_000.00
    dotô = Diretor(Americanas)
    print(f'{zé.salário()=:_.2f}')
    print(f'{Enzo.salário()=:_.2f}')
    print(f'{dotô.salário()=:_.2f}')
    print('-'*50)
