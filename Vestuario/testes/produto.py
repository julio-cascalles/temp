from fastapi.testclient import TestClient
from testes.dados import MOCK_PRODUTO_AVULSO
from modelos.util.categorias import Categoria
from urllib.parse import urlencode


def grava_produto(client: TestClient) -> bool:
    res = client.post('/produto', json=MOCK_PRODUTO_AVULSO)
    if res.status_code != 200:
        return False
    # --- Consulta o produto para ver se gravou certo: ------
    busca = urlencode({'nome': MOCK_PRODUTO_AVULSO['categoria']})
    res = client.get(f'/produtos/{busca}')
    if res.status_code != 200:
        return False
    gravado = res.json()[0]
    for campo in ('nome', 'valor'):
        if gravado[campo] != MOCK_PRODUTO_AVULSO[campo]:
            return False
    return True
    # -------------------------------------------------------
