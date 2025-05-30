from fastapi.testclient import TestClient


def get_headers(client: TestClient, dados:dict) -> dict:
    res = client.post("/login", json=dict(
        username=dados['email'],
        password=dados['senha'],
    ))
    if res.status_code != 200:
        return None
    token = res.json()['access_token']
    return {"Authorization": f"Bearer {token}"}
