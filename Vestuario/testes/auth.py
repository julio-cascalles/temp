from fastapi.testclient import TestClient
from testes.dados import MOCK_AUTH
from uuid import uuid4
from testes.util.login import get_admin
from enum import Enum
from modelos.auth import CAMPO_SENHA_TEMP
from urllib.parse import urlencode


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

class RetornoAdmin(Enum):
    ADMIN_GRAVOU_TUDO_OK = 0
    ADMIN_ERR_VALIDACAO  = 2
    ADMIN_ERR_NAO_ACHOU  = 3
    ADMIN_LOGIN_INVALIDO = 4

def primeiro_acesso(client: TestClient) -> RetornoAdmin:
    PERSONAGEM_PRINCIPAL = "SpongeBob Squarepants"
    NOVA_SENHA_BOB = 'Abc123'
    res = client.post('/admin/novos_usuarios', json=[
        PERSONAGEM_PRINCIPAL, "Patrick Star",
        "Mr Krabs", "Squidward Tentacles", "Sandy Cheeks"
    ], headers=get_admin(client))
    if res.status_code != 200:
        return RetornoAdmin.ADMIN_ERR_VALIDACAO
    # ------ Vê se Bob consegue alterar sua senha -------
    bob = res.json()[PERSONAGEM_PRINCIPAL]
    loginForm = dict(
        username=bob['email'],
        password=bob[CAMPO_SENHA_TEMP],
    )
    params = urlencode({   
        k: NOVA_SENHA_BOB
        for k in ('nova_senha', 'confirmacao')
    })
    res = client.put(f'/mudar_senha?{params}', json=loginForm)
    if res.status_code != 200:
        return RetornoAdmin.ADMIN_ERR_NAO_ACHOU
    # --- Agora tenta fazer o login com a senha nova: ---
    loginForm['password'] = NOVA_SENHA_BOB
    res = client.post("/login", json=loginForm)
    if res.status_code != 200:
        return RetornoAdmin.ADMIN_LOGIN_INVALIDO
    return RetornoAdmin.ADMIN_GRAVOU_TUDO_OK
