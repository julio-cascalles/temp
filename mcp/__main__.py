# from interface.server import Server
from interface.client import procurar_veiculo


def main():
    print(
        procurar_veiculo(
            marca="Honda",
            modelo="Fit",
            cor="azul",
        )
    )


main()