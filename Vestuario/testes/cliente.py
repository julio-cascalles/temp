from fastapi.testclient import TestClient
from testes.dados import MOCK_CLIENTE_AVULSO
from urllib.parse import urlencode
from modelos.util.categorias import Categoria
from modelos.util.midias import Midia


def grava_cliente(client: TestClient):
    res = client.post('/cliente', json=MOCK_CLIENTE_AVULSO)
    if res.status_code != 200:
        return False
    # --- Consulta o cliente para ver se gravou certo: ------
    busca = urlencode( dict(nome=MOCK_CLIENTE_AVULSO['nome']) )
    res = client.get(f'/clientes?{busca}')
    if res.status_code != 200:
        return False
    gravado = res.json()[0]
    CAMPOS_E_CLASSES = {
        'preferencias': Categoria,
        'redes_sociais': Midia
    }
    for campo, classe in CAMPOS_E_CLASSES.items():
        flag = classe.combo(MOCK_CLIENTE_AVULSO[campo])
        if gravado[campo] != flag:
            return False
    return True
    # -------------------------------------------------------
