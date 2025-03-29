from dados.veiculo import Veiculo
from rotas.server import Server
from threading import Thread


def retornar_consulta(filtros: dict):
    return [
        str(carro)
        for carro in Veiculo.find(**filtros)
    ]

def executa():
    Server(retornar_consulta)
