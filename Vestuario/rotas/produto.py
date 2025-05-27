from fastapi import APIRouter, Depends, HTTPException, status
from modelos.produto import Produto
from modelos.util.categorias import Categoria


router = APIRouter()

@router.post('/produto')
def grava_produto(produto: Produto):
    """
    Grava um produto avulso.
    Você também pode gravar produtos através
    de campanhas de *Lançamento*: `/campanha/lancamento`
    """
    duplicado = Produto.find(nome=produto.nome)
    if duplicado:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe um produto com este nome."
        )
    produto.save()
    return 'Produto gravado com sucesso'

@router.get('/categorias')
def lista_categorias():
    """
    Lista todas as categorias reconhecidas pelo sistema.
    """
    return [c.name for c in Categoria]

@router.get('/produtos/{categorias}')
def consulta_produtos(categorias):
    """
    Traz os produtos que mais tem as categorias procuradas.
    Exemplo: `/produtos/ROUPA+FEMININA+PRAIA`
    """
    busca = Categoria.combo(categorias)
    def similaridade(produto: Produto) -> int:
        s1 = set(produto.categoria)
        s2 = set(busca)
        return len( s1.intersection(s2) )
    encontrados = Produto.find(
        categoria={'$in': busca}
    )
    if not encontrados:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Nenhum produto encontrado nesta busca.'
        )
    encontrados.sort(key=lambda p: similaridade(p), reverse=True)
    return encontrados
