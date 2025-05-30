from fastapi.testclient import TestClient
from rotas.util.app import create_app
from modelos.util.mongo_table import MongoTable, TEST_DATABASE
from testes.auth import registra_usuario_ok, registra_usuario_falha
from testes.campanha import lancamento, prospeccao, liquidacao, encerrar_campanha
from testes.cliente import grava_cliente
from testes.produto import grava_produto
from testes.dados import MOCK_AUTH, MOCK_AUTH2
from testes.util.login import get_headers


client = TestClient(
    create_app()
)
MongoTable.DATABASE_NAME = TEST_DATABASE


def test_auth_sucesso():
    assert registra_usuario_ok(client)
    client.__annotations__['headers'] = get_headers(client, MOCK_AUTH)

def test_auth_falha():
    assert registra_usuario_falha(client)

def test_lancamento():
    assert lancamento(client)

def test_prospeccao():
    assert prospeccao(client)

def test_liquidacao():
    assert liquidacao(client)

def test_cliente():
    assert grava_cliente(client)

def test_falha_produto():
    """
    Testa quando o usuário não tem permissão para gravar produto:
    """
    assert grava_produto(client) #--- Retorna TRUE porque está esperando um erro.

def test_produto():
    assert grava_produto(client,  get_headers(client, MOCK_AUTH2))
    #                                                   ^^^
    #                                                    |
    #   Usuário com acesso para gravar produtos ---------+

def test_encerrar_campanha():
    assert encerrar_campanha(client)
