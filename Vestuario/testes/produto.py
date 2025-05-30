from enum import Enum
from fastapi.testclient import TestClient
from testes.dados import MOCK_PRODUTO_AVULSO
from urllib.parse import urlencode


class Retorno(Enum):
    PRODUTO_GRAVOU_TUDO_OK = 0
    PRODUTO_ERR_SEM_ACESSO = 1
    PRODUTO_ERR_VALIDACAO  = 2
    PRODUTO_ERR_NAO_ACHOU  = 3
    PRODUTO_ERR_DETALHES   = 4


def grava_produto(client: TestClient, headers: dict=None) -> Retorno:
    nao_autorizado = headers is None
    if nao_autorizado:
        headers = client.__annotations__['headers']
    res = client.post(
        '/produto', json=MOCK_PRODUTO_AVULSO, headers=headers
    )
    if res.status_code != 200:
        if nao_autorizado:
            return Retorno.PRODUTO_ERR_SEM_ACESSO
        else:
            return Retorno.PRODUTO_ERR_VALIDACAO
    # --- Consulta o produto para ver se gravou certo: ------
    busca = urlencode({'nome': MOCK_PRODUTO_AVULSO['categoria']})
    res = client.get(f'/produtos/{busca}')
    if res.status_code != 200:
        return Retorno.PRODUTO_ERR_NAO_ACHOU
    gravado = res.json()[0]
    for campo in ('nome', 'valor'):
        if gravado[campo] != MOCK_PRODUTO_AVULSO[campo]:
            return Retorno.PRODUTO_ERR_DETALHES
    return Retorno.PRODUTO_GRAVOU_TUDO_OK
    # -------------------------------------------------------
