from fastapi.testclient import TestClient
from testes.dados import MOCK_AUTH
from uuid import uuid4


def registra_usuario_ok(client: TestClient, dados: dict) -> bool:
    res = client.post("/registra_usuario", json=dados)
    return res.status_code == 200

def registra_usuario_falha(client: TestClient) -> bool:
    """
    Tenta cadastrar várias vezes o mesmo usuário:
    """
    dados = {
        'email': 'teste_{}@xyz.com'.format(
            str(uuid4())  # --- Email único para não conflitar com MOCK_AUTH
        ),
        'senha': 'QQ_C01sa',
        'nome': 'Fake de oliveira'
    }
    for i in range(2):
        res = client.post("/registra_usuario", json=dados)
    return res.status_code == 400

def primeiro_acesso(client: TestClient) -> bool:
    res = client.post('/admin/novos_usuarios', json=[
        "SpongeBob Squarepants", "Patrick Star",
        "Mr Krabs", "Squidward Tentacles", "Sandy Cheeks"
    ])
    if res.status_code != 200:
        return False
    return True
