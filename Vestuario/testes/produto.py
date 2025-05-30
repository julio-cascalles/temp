from fastapi.testclient import TestClient
from testes.dados import MOCK_PRODUTO_AVULSO
from urllib.parse import urlencode


def grava_produto(client: TestClient, headers: dict=None) -> bool:
    expected_status = 200
    if not headers:
        expected_status = 405 # --- O usuário padrão NÃO tem acesso para gravar produto!
        headers = client.__annotations__['headers']
    res = client.post(
        '/produto', json=MOCK_PRODUTO_AVULSO, headers=headers
    )
    if res.status_code != 200:
        return res.status_code == expected_status
    # --- Consulta o produto para ver se gravou certo: ------
    busca = urlencode({'nome': MOCK_PRODUTO_AVULSO['categoria']})
    res = client.get(f'/produtos/{busca}')
    if res.status_code != expected_status:
        return False
    gravado = res.json()[0]
    for campo in ('nome', 'valor'):
        if gravado[campo] != MOCK_PRODUTO_AVULSO[campo]:
            return False
    return True
    # -------------------------------------------------------
