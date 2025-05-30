from fastapi import APIRouter, Depends, HTTPException, status
from modelos.cliente import Cliente
from modelos.util.categorias import Categoria
from modelos.util.midias import Midia
from modelos.auth import Usuario
from rotas.auth import usuario_da_sessao
from modelos.util.acesso import Permissao


router = APIRouter()

@router.post('/cliente')
def grava_cliente(cliente: Cliente, user:Usuario=Depends(usuario_da_sessao)):
    """
    Grava um cliente avulso.
    Você também pode gravar clientes através
    de campanhas de *Prospecção*: `/campanha/prospeccao`
    """
    if Permissao.post_cliente not in user.permissoes:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail='Seu usuário não tem permissão para este recurso.'
        )
    duplicado = Cliente.find(email=cliente.email)
    if duplicado:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este email já está em uso!"
        )
    cliente.save()
    return 'Cliente gravado com sucesso.'

@router.get('/clientes')
def consulta_clientes(
    nome: str='',
    preferencias: str='',
    redes_sociais: str=''
):
    """
    Consulta clientes por nome parecido, preferências
    de produtos ou quais redes sociais ele possui.
    """
    query = {}
    # --- Monta a query: ------------------------------
    if nome:
        query['nome'] = {'$regex': f'.*{nome}.*'}
    if preferencias:
        query['preferencias'] = {'$in': Categoria.combo(preferencias)}
    if redes_sociais:
        query['redes_sociais'] = {'$in': Midia.combo(redes_sociais)}
    # --------------------------------------------------
    if not query:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="""
            Especifique um critério da pesquisa:
            * email = Traz os clientes cujo email coincide com a busca
            * redes_sociais = Clientes que tem determinadas redes sociais
            * preferencias = Clientes que gostam de certos tipos de produtos
                > (para maiores informações use `/categorias`)
            """
        )
    return Cliente.find(**query)

@router.get('/midias')
@router.get('/redes_sociais')
def redes_sociais():
    """
    Lista todas as mídias (ou redes sociais)
    reconhecidas por este sistema.
    """
    return [c.name for c in Midia]
