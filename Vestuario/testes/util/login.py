from fastapi.testclient import TestClient
from modelos.util.acesso import ADMIN_PADRAO


def header_from_resp(resp) -> dict:
    token = resp.json()['access_token']
    return {"Authorization": f"Bearer {token}"}

def get_headers(client: TestClient, dados:dict) -> dict:
    res = client.post("/login", json=dict(
        username=dados['email'],
        password=dados['senha'],
    ))
    if res.status_code != 200:
        return None
    return header_from_resp(res)

def get_admin(client: TestClient) -> dict:
    res = client.post("/registra_usuario", json=ADMIN_PADRAO)
    if res.status_code != 200:
        return None
    return header_from_resp(res)
