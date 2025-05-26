from fastapi import APIRouter, Depends, HTTPException, status
from modelos.cliente import Cliente
from modelos.util.categorias import Categoria
from modelos.util.midias import Midia


router = APIRouter()

@router.post('/cliente')
def grava_cliente(cliente: Cliente):
    duplicado = Cliente.find_first(email=cliente.email)
    if duplicado:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este email já está em uso!"
        )
    cliente.save()

@router.get('/clientes')
def consulta_clientes(
    email: str='',
    preferencias: str='',
    redes_sociais: str=''
):
    query = {}
    # --- Monta a query: ------------------------------
    if email:
        query['email'] = {'$regex': f'.*{email}.*'}
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

@router.get('/categorias')
def redes_sociais():
    return [c.name for c in Midia]
