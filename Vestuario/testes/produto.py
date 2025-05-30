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


def grava_produto(client: TestClient, header_idx: int=1) -> Retorno:
    nao_autorizado = (header_idx == 1)
    #                   ^^^
    #                    |
    #                    +----------- O usuário padrão 
    #                                 não está autorizado
    #                                 a gravar produtos.
    headers = client.__annotations__[f'headers{header_idx}']
    res = client.post(
        '/produto', json=MOCK_PRODUTO_AVULSO, headers=headers
    )
    if res.status_code != 200:
        if nao_autorizado and res.status_code == 405:
            return Retorno.PRODUTO_ERR_SEM_ACESSO
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
