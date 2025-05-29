from fastapi.testclient import TestClient
from testes.dados import MOCK_AUTH


def get_header(client: TestClient) -> dict:
    res = client.post("/login", json=dict(
        username=MOCK_AUTH['email'],
        password=MOCK_AUTH['senha'],
    ))
    if res.status_code != 200:
        return False
    token = res.json()['access_token']
    return {"Authorization": f"Bearer {token}"}
