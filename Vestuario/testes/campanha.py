from fastapi.testclient import TestClient
from urllib.parse import urlencode
from testes.dados import MOCK_LANCAMENTO, MOCK_LIQUIDACAO, MOCK_PROSPECCAO
from modelos.produto import Produto
from modelos.cliente import Cliente
from modelos.util.categorias import Categoria


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

def liquidacao(client: TestClient) -> bool:
    res = client.post('/campanha/liquidacao', json=MOCK_LIQUIDACAO)
    if res.status_code != 200:
        return False
    # --- Consulta se a campanha foi realmente gravada: ----
    busca = urlencode( dict(nome=MOCK_LIQUIDACAO['nome']) )
    res = client.get(f'/campanhas?{busca}')
    if res.status_code != 200:
        return False
    # --- Verfica se os dados da campanha estão corretos: ----
    desconto = res.json()[0]['desconto']
    if MOCK_LIQUIDACAO['desconto'] != desconto:
        return False
    encontrado = Produto.find(
        categoria={'$in': Categoria.combo(MOCK_LIQUIDACAO['categorias'])}
    )
    if not encontrado:
        return False
    produto: Produto
    for produto in encontrado:
        if not produto.cupom or produto.cupom['desconto'] !=  desconto:
            return False
    # -----------------------------------------------------------------
    return True

def encerrar_campanha(client: TestClient) -> bool:
    busca = '2026' # <-- MOCK_LANCAMENTO & MOCK_PROSPECCAO
    res = client.delete(f'/encerrar_campanha/{busca}')
    if res.status_code != 200:
        return False
    res = client.get(f'/campanhas?{busca}')
    # ---- Não pode encontrar as campanhas excluídas -----
    return res.status_code == 400

