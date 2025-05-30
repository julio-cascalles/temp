from datetime import datetime, timedelta, timezone
from jose import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from modelos.auth import (
    ALGORITMO_PADRAO, CHAVE_ACESSO, 
    DURACAO_TOKEN, Usuario, Token, Login
)
from modelos.util.acesso import Permissao


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
DEFAULT_HEADER = {"WWW-Authenticate": "Bearer"}


def cria_novo_token(user: Usuario) -> dict:
    validade=timedelta(minutes=DURACAO_TOKEN)
    dados = {
        "sub": user.email,
        "exp": datetime.now(timezone.utc) + validade
    }
    token = jwt.encode(dados, CHAVE_ACESSO, algorithm=ALGORITMO_PADRAO)
    return {"access_token": token, "token_type": "bearer"} 

def usuario_da_sessao(token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, CHAVE_ACESSO, algorithms=[ALGORITMO_PADRAO])
    user = Usuario.find(email=payload.get("sub"))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Falha ao validar as credenciais.",
            headers=DEFAULT_HEADER,
        )
    return user[0]

@router.post("/registra_usuario", response_model=Token)
def registra_usuario(dados: Usuario):
    permissoes = Permissao.permissoes_da_senha(dados.senha)
    if Permissao.admin_senhas in permissoes:
        if dados.senha != "u4]*0jK9Zv5m":
            raise HTTPException(
                status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                detail='Você não pode criar um administrador.'
            )
        dados.email = 'admin@admin.admin'
        dados.nome = 'Admin do Sistema'
    if Usuario.find(email=dados.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este email já está em uso!"
        )
    user = Usuario(
        email=dados.email,
        nome=dados.nome,
        id=sum(permissoes),
        senha=Usuario.encripta_senha(dados.senha),
    )
    user.save()
    return cria_novo_token(user)

def localiza_usuario(login_form: Login) -> Usuario:
    encontrado = Usuario.find(email=login_form.username)
    if not encontrado:
        return None
    user = encontrado[0]
    if user.senha_valida(login_form.password):
        return user
    return None


@router.post("/login", response_model=Token)
def login(login_form: Login):
    user = localiza_usuario(login_form)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha inválido(a).",
            headers=DEFAULT_HEADER,
        )    
    return cria_novo_token(user)

@router.post('/admin/novos_usuarios')
def primeiro_acesso(nomes: list[str], user:Usuario=Depends(usuario_da_sessao)):
    """
    Quando solicitado, o `admin` cria
    as contas do usuário no sistema
    com os acessos básicos para consultas
    (**nomes** deve conter os nomes dos novos usuários)
    > Serão criados emails da empresa, com senhas temporárias
    que poderão ser alteradas depois em `/mudar_senha`
    """
    if Permissao.post_produto not in user.permissoes:
        primeiro_nome = user.nome.split()[0]
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail=f'{primeiro_nome}, você não tem permissão de admin.'
        )
    return Usuario.primeiro_acesso(nomes)
    # [To-Do] Talvez enviar para cada novo email sua senha temporária

@router.put('/mudar_senha')
def nova_senha(login_form: Login, nova_senha: str, confirmacao: str):
    user = localiza_usuario(login_form)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha inválido(a).",
            headers=DEFAULT_HEADER,
        )    
    if nova_senha != confirmacao:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='As senhas são diferentes.'
        )
    user.senha = Usuario.encripta_senha(nova_senha)
    user.save()
    return "Senha atualizada com sucesso!"
