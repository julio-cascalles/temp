from fastapi.testclient import TestClient
from rotas.util.app import create_app
from modelos.util.mongo_table import MongoTable, TEST_DATABASE
from testes.auth import (
    registra_usuario_ok, registra_usuario_falha,
    primeiro_acesso, RetornoAdmin
)
from testes.campanha import lancamento, prospeccao, liquidacao, encerrar_campanha
from testes.cliente import grava_cliente
from testes.produto import grava_produto, RetornoProduto
from testes.dados import MOCK_AUTH, MOCK_AUTH2
from testes.util.login import get_headers


client = TestClient(
    create_app()
)
MongoTable.DATABASE_NAME = TEST_DATABASE


def test_auth_sucesso():
    for i, dados in enumerate([MOCK_AUTH, MOCK_AUTH2], start=1):
        assert registra_usuario_ok(client, dados)
        client.__annotations__[f'headers{i}'] = get_headers(client, dados)

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
    assert grava_produto(client) == RetornoProduto.PRODUTO_ERR_SEM_ACESSO

def test_produto():
    USUARIO_COM_ACESSO_GRAVAR_PROD = 2
    assert RetornoProduto.PRODUTO_GRAVOU_TUDO_OK == grava_produto(
        client, USUARIO_COM_ACESSO_GRAVAR_PROD
    )

def test_encerrar_campanha():
    assert encerrar_campanha(client)

def test_primeiro_acesso():
    assert RetornoAdmin.ADMIN_GRAVOU_TUDO_OK == primeiro_acesso(client)
