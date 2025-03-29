import socket
import json
from rotas.const import HOST, PORT


def read_mcp(filter: dict) -> dict:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    dados = json.dumps(filter)
    client.send(dados.encode())
    res = client.recv(4096).decode()
    client.close()
    if not res:
        return ['''
        ************************************
                Nenhum registro encontrado
        ************************************
        ''']
    return json.loads(res)
