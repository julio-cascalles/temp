from fastapi import FastAPI
from rotas  import auth, campanha, cliente, produto


def create_app():
    app = FastAPI()
    app.include_router(auth.router)
    app.include_router(campanha.router)
    app.include_router(cliente.router)
    app.include_router(produto.router)
    return app
