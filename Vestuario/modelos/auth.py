import os
from dotenv import load_dotenv
from passlib.context import CryptContext
from pydantic import BaseModel, field_validator
from modelos.util.mongo_table import MongoTable


load_dotenv()
cypt_ctx = CryptContext(
    schemes=["bcrypt"], deprecated="auto"
)


CHAVE_ACESSO = os.getenv("CHAVE_ACESSO", "senha-padrao")
ALGORITMO_PADRAO = "HS256"
DURACAO_TOKEN = 30


class Token(BaseModel):
    access_token: str
    token_type: str


class Usuario(BaseModel, MongoTable):
    email: str
    nome: str
    senha: str

    @staticmethod
    def encripta_senha(nova_senha: str) -> str:
        # return cypt_ctx.encrypt(nova_senha)
        return cypt_ctx.hash(nova_senha)

    def senha_valida(self, senha: str) -> bool:
        if not cypt_ctx.verify(senha):
            return False
        return self.senha == senha

