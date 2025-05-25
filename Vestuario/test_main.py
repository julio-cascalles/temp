from fastapi.testclient import TestClient
from rotas.util.app import create_app
from modelos.util.mongo_table import MongoTable, TEST_DATABASE
from testes.auth import cadastra_usuario_sucesso, falha_cadastro_dupl


client = TestClient(
    create_app()
)
MongoTable.DATABASE_NAME = TEST_DATABASE


def test_auth_sucesso():
    assert cadastra_usuario_sucesso(client)

def test_auth_falha():
    assert falha_cadastro_dupl(client)
