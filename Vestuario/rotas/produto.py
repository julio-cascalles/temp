from fastapi import APIRouter, Depends, HTTPException, status
from modelos.produto import Produto
from modelos.util.categorias import Categoria


router = APIRouter()

@router.post('/produto')
def grava_produto(produto: Produto):
    duplicado = Produto.find(nome=produto.nome)
    if duplicado:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe um produto com este nome."
        )
    produto.save()

@router.get('/categorias')
def lista_categorias():
    return [c.name for c in Categoria]

@router.get('/produtos/{categorias}')
def consulta_produtos(categorias):
    encontrados = Produto.find(
        categoria={'$in': categorias},
        estoque={'$gt': 1}
    )
    if not encontrados:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Nenhum produto encontrado nesta busca.'
        )
    return encontrados
