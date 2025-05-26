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

@router.get('/categorias')
def lista_categorias():
    """
    Lista todas as categorias reconhecidas pelo sistema.
    """
    return [c.name for c in Categoria]

@router.get('/produtos/{categorias}')
def consulta_produtos(categorias):
    """
    Pesquise várias categorias em que os produtos podem estar.
    Você pode usar vírgula, traço ou qualquer sinal para separar
    as categorias da busca. Exemplo:
        `/produtos/ROUPA+FEMININA+PRAIA`
            * Biquini
            * Saída de banho
            * Maiô
        > Obs.: Não use os caracteres reservados de URL
                ("/", "&", ":", "%", ".", "?" ...)
    """
    encontrados = Produto.find(
        categoria={'$in': Categoria.combo(categorias)}
    )
    if not encontrados:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Nenhum produto encontrado nesta busca.'
        )
    return encontrados
