from datetime import datetime, timedelta, timezone
from jose import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from modelos.auth import (
    ALGORITMO_PADRAO, DURACAO_TOKEN,
    CHAVE_ACESSO, User, UserData, Token
)


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
DEFAULT_HEADER = {"WWW-Authenticate": "Bearer"}


def cria_novo_token(user: User) -> dict:
    validade=timedelta(minutes=DURACAO_TOKEN)
    dados = {
        "sub": user.email,
        "exp": datetime.now(timezone.utc) + validade
    }
    token = jwt.encode(dados, CHAVE_ACESSO, algorithm=ALGORITMO_PADRAO)
    return {"access_token": token, "token_type": "bearer"} 

def usuario_da_sessao(token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, CHAVE_ACESSO, algorithms=[ALGORITMO_PADRAO])
    user = User.find_first(email=payload.get("sub"))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Falha ao validar as credenciais.",
            headers=DEFAULT_HEADER,
        )
    return user

@router.post("/registra_usuario", response_model=Token)
def registra_usuario(dados: UserData):
    if User.find_first(email=dados.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este email já está em uso!"
        )
    user = User(
        email=dados.email,
        nome=dados.nome,
        senha=User.encripta_senha(dados.senha)
    )
    user.save()
    return cria_novo_token(user)

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = User.find_first(email=form_data.username)
    if not user or not user.senha_valida(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha inválido(a).",
            headers=DEFAULT_HEADER,
        )    
    return cria_novo_token(user)
