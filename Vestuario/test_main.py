from fastapi.testclient import TestClient
from rotas.util.app import create_app
from modelos.util.mongo_table import MongoTable, TEST_DATABASE
# from testes.auth import cadastra_usuario_sucesso, falha_cadastro_dupl
from testes.campanha import lancamento, prospeccao, liquidacao, encerrar_campanha
from testes.cliente import grava_cliente
from testes.produto import grava_produto


client = TestClient(
    create_app()
)
MongoTable.DATABASE_NAME = TEST_DATABASE


# def test_auth_sucesso():
#     assert cadastra_usuario_sucesso(client)

# def test_auth_falha():
#     assert falha_cadastro_dupl(client)

def test_lancamento():
    assert lancamento(client)

def test_prospeccao():
    assert prospeccao(client)

def test_liquidacao():
    assert liquidacao(client)

def test_cliente():
    assert grava_cliente(client)

def test_produto():
    assert grava_produto(client)

def test_encerrar_campanha():
    assert encerrar_campanha(client)

