from fastapi.testclient import TestClient
from modelos.auth import Usuario
from uuid import uuid4


TEST_USER_NOME = "Usuário de Teste"
TEST_USER_SENHA = "senhaSegura123"


def cadastra_usuario_sucesso(client: TestClient) -> bool:
    user = Usuario(
        nome=TEST_USER_NOME,
        senha=TEST_USER_SENHA,
        email= '{}.@xyz.com'.format( uuid4() )
    )
    response = client.post("/cadastrar", json=user.model_dump())
    return response.status_code == 200

def falha_cadastro_dupl(client: TestClient) -> bool:
    for i in range(2):
        user = Usuario(
            nome=TEST_USER_NOME,
            senha=TEST_USER_SENHA,
            email='email-repetido@xyz.com'
        )
        response = client.post("/cadastrar", json=user.model_dump())
        if i == 0:
            continue
        return response.status_code == 200
