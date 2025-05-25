from fastapi import APIRouter, Depends, HTTPException, status
from modelos.cliente import Cliente


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
    preferencias: list=None,
    redes_sociais: list=None
):
    query = {}
    # --- Monta a query: ------------------------------
    if email:
        query['email'] = {'$regex': f'.*{email}.*'}
    if preferencias:
        query['preferencias'] = {'$in': preferencias}
    if redes_sociais:
        query['redes_sociais'] = {'$in': redes_sociais}
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
