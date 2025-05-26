from fastapi import APIRouter, Depends, HTTPException, status
from modelos.campanha import Campanha, TipoCampanha
from modelos.util.categorias import Categoria
from modelos.util.midias import Midia
from modelos.cliente import Cliente


router = APIRouter()

@router.post('/campanha')
def grava_campanha(campanha: Campanha):
    duplicada = Campanha.find(nome=campanha.nome)
    if duplicada:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe uma campanha com este nome."
        )
    campanha.save()

@router.get('/campanhas')
def consulta_campanhas(
    tipo: TipoCampanha=None,
    categorias: str='',
    midias: str=''
):
    query = {}
    # ---- Monta a query: ----------------------
    if tipo:
        query['tipo'] = tipo
    if categorias:
        query['categorias'] = {'$in': Categoria.combo(categorias)}
    if midias:
        query['midias'] = {'$in': Midia.combo(midias)}
    # ------------------------------------------
    if not query:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="""
            Especifique um critério da pesquisa:
            * tipo = Traz as campanhas do tipo procurado
                > para mais detalhes, veja `/tipos_campanha`
            * categorias = Campanhas que promovem certas cat. de produtos
                > (para maiores informações use `/categorias`)
            * midias = Em quais mídias as campanhas serão divulgadas
                > (para maiores informações use `/midias`)
            """
        )
    return Campanha.find(**query)

@router.get('/publico_alvo/{nome_campanha}')
def publico_alvo(nome_campanha: str):
    campanha = Campanha.find_first(nome=nome_campanha)
    if not campanha:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Nenhuma campanha encontrada nesta busca.'
        )
    encontrados = Cliente.find(
        preferencias=campanha.categorias,
        redes_sociais=campanha.midias
    )
    if not encontrados:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Nenhum cliente é compatível com esta campanha.'
        )
    return encontrados
