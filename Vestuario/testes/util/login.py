from fastapi.testclient import TestClient
from testes.dados import MOCK_ADMIN


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
    res = client.post("/registra_usuario", json=MOCK_ADMIN)
    if res.status_code != 200:
        return None
    return header_from_resp(res)
