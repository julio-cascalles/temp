from dados.veiculo import Veiculo


MINIMO =  100
MAXIMO = 5000

def valida(valor: int) -> bool:
    if valor < MINIMO:
        print(f"Valor mínimo é {MINIMO}.")
        return False
    if valor > MAXIMO:
        print(f"Valor máximo é {MAXIMO}.")
        return False
    return True


def executa():
    quantidade = 0
    while not valida(quantidade):
        try:
            quantidade = int(input("Quantos veículos deseja criar? "))
        except ValueError:
            print("A quantidade deve ser um valor numérico.")
    print('-' * 50)
    print(f"Gerando {quantidade} veículos...")
    Veiculo.populate(quantidade)
    print("Veículos gerados com sucesso.".center(50, '*'))
    print('*' * 50)
