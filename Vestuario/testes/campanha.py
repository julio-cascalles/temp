from fastapi.testclient import TestClient
from urllib.parse import urlencode
from testes.dados import MOCK_LANCAMENTO, MOCK_PROSPECCAO
from modelos.produto import Produto
from modelos.cliente import Cliente


def lancamento(client: TestClient) -> bool:
    res = client.post('/campanha/lancamento', json=MOCK_LANCAMENTO)
    if res.status_code != 200:
        return False
    # --- Consulta se a campanha foi realmente gravada: ----
    busca = urlencode( dict(nome=MOCK_LANCAMENTO['nome']) )
    res = client.get(f'/campanhas?{busca}')
    if res.status_code != 200:
        return False
    produtos_novos = res.json()[0]['produtos']
    # ------------------------------------------------------
    # --- Verifica se todos os produtos estão corretos: ----
    if len(produtos_novos) != len(MOCK_LANCAMENTO['produtos']):
        return False
    for item in produtos_novos:
        encontrado = Produto.find(nome=item['nome'])
        if not encontrado:
            return False
        produto = encontrado[0]
        if item['valor'] != produto.valor:
            return False
    # ------------------------------------------------------
    return True

def prospeccao(client: TestClient) -> bool:
    res = client.post('/campanha/prospeccao', json=MOCK_PROSPECCAO)
    if res.status_code != 200:
        return False
    # --- Consulta se a campanha foi realmente gravada: ----
    busca = urlencode( dict(nome=MOCK_PROSPECCAO['nome']) )
    res = client.get(f'/campanhas?{busca}')
    if res.status_code != 200:
        return False
    # --- Verfica se todos os clientes estão corretos: ----
    clientes_novos = res.json()[0]['clientes']
    if len(clientes_novos) != len(MOCK_PROSPECCAO['clientes']):
        return False
    for item in clientes_novos:
        encontrado = Cliente.find(nome=item['nome'])
        if not encontrado:
            return False
        cliente = encontrado[0]
        if item['email'] != cliente.email:
            return False
    # ------------------------------------------------------
    return True
