from dataclasses import dataclass

@dataclass
class ItemMochila:
    nome: str
    volume: float
    importancia: int

    @property
    def eficiencia(self) -> float:
        return self.importancia / self.volume


@dataclass
class Mochila:
    capacidade: int

    def levar(self, item: ItemMochila) -> bool:
        self.capacidade -= item.volume
        return self.capacidade > 0

    def itens_que_cabem(self, todos_itens: list[ItemMochila]) -> list:
        todos_itens.sort(key=lambda x: x.eficiencia, reverse=True)
        return [item for item in todos_itens if self.levar(item)]



if __name__ == '__main__':
    import sys
    tamanho = int(
        sys.argv[1] if len(sys.argv) > 1
        else input('Tamanho da mochila:')
    )
    selecionados = Mochila(tamanho).itens_que_cabem([
      ItemMochila('Guarda-chuva', 10, 6),
      ItemMochila('Garrafa de água', 2, 4),
      ItemMochila('Óculos', 1, 9),
      ItemMochila('Blusa', 8, 5),
      ItemMochila('Porta escova de dentes', 2, 7),
      ItemMochila('Marmita', 7, 9),
      ItemMochila('Livro', 4, 1),
      ItemMochila('Estojo remédios', 3, 2),
    ])
    print('-'*50)
    for item in selecionados:
        print(item.nome)
    print('-'*50)
