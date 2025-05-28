from fastapi.testclient import TestClient
from testes.dados import MOCK_AUTH
from uuid import uuid4


def registra_usuario_ok(client: TestClient) -> bool:
    dados = MOCK_AUTH
    dados['email'] = 'teste_{}@xyz.com'.format(
        str(uuid4)  # --- Email único para não dar erro
    )
    res = client.post("/registra_usuario", json=dados)
    return res.status_code == 200

def registra_usuario_falha(client: TestClient) -> bool:
    """
    Tenta cadastrar 2 vezes o mesmo usuário:
    """
    for i in range(2):
        res = client.post("/registra_usuario", json=MOCK_AUTH)
    return i == 1  and res.status_code == 400