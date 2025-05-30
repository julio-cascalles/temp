import os
from dotenv import load_dotenv
from passlib.context import CryptContext
from pydantic import BaseModel, field_validator
from modelos.util.mongo_table import MongoTable
from modelos.util.acesso import Permissao


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


class Login(BaseModel):
    username: str
    password: str


SUFIXO_EMAIL_COMPANHIA = 'bikinibottom.net'
ACESSOS_BASICOS = [
    Permissao.get_categorias, Permissao.get_clientes,
    Permissao.get_midias, Permissao.get_produtos
] # --- Somente acessos de consulta

class Usuario(BaseModel, MongoTable):
    email: str
    nome: str
    senha: str
    id: int=0

    @staticmethod
    def encripta_senha(nova_senha: str) -> str:
        return cypt_ctx.hash(nova_senha)

    def senha_valida(self, senha_digitada: str) -> bool:
        return cypt_ctx.verify(senha_digitada, self.senha)

    @property
    def permissoes(self):
        return Permissao(self.id)

    @classmethod
    def primeiro_acesso(cls, nomes: list, acessos: list=ACESSOS_BASICOS) -> list:
        criados = []
        for nome in nomes:
            temp = Permissao.cria_senha(acessos)
            novo = cls(
                email='{}@{}'.format(
                    '-'.join(nome.lower().split()),
                    SUFIXO_EMAIL_COMPANHIA
                ),
                nome=nome, senha=Usuario.encripta_senha(senha),
                id=sum(acessos),
            )
            novo.save()
            criados.append({
                'email': novo.email,
                'senha temporária': temp
            })
        return criados
