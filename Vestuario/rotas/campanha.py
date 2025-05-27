from fastapi import APIRouter, Depends, HTTPException, status
from modelos.campanha import Campanha, Lancamento, Liquidacao, Prospeccao
from modelos.util.categorias import Categoria
from modelos.util.midias import Midia
from modelos.cliente import Cliente


router = APIRouter()


def verifica_duplicada(campanha: Campanha):
    if Campanha.find_all(nome=campanha.nome):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe uma campanha com este nome."
        )

# ------- Grava por tipo de Campanha: ------------
@router.post('/campanha/lancamento')
def lancamento(campanha: Lancamento):
    """
    Faz o lançamento dos novos produtos,
    deixando-os disponíveis para consumo:
    """
    verifica_duplicada(campanha)
    if not campanha.save():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nenhum produto pode ser lançado.", 
        )
    return 'Campanha criada com sucesso!'

@router.post('/campanha/liquidacao')
def liquidacao(campanha: Liquidacao):
    """
    Aplica cupom de desconto em
    todos os produtos da campanha
    """
    verifica_duplicada(campanha)
    if not campanha.save():
        raise HTTPException(
            detail='Nenhum produto encontrado para receber o cupom.',
            status_code=status.HTTP_400_BAD_REQUEST
        )

@router.post('/campanha/prospeccao')
def prospeccao(campanha: Prospeccao):
    """
    Converte `leads` em clientes
    """
    verifica_duplicada(campanha)
    campanha.save()
# -------------------------------------------------

@router.get('/campanhas')
def consulta_campanhas(
    nome: str='',
    categorias: str='',
    midias: str=''
):
    query = {}
    # ---- Monta a query: ----------------------
    if nome:
        query['nome'] = {'$regex': f'.*{nome}.*'}
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
            * nome = Busca campanhas que contém o nome procurado;
            * categorias = Campanhas relacionadas a categorias de prod.
                > (para maiores informações use `/categorias`)
            * midias = Em quais mídias as campanhas serão divulgadas
                > (para maiores informações use `/midias`)
            """
        )
    return Campanha.find_all(**query)


@router.delete('/encerrar_campanha/{nome_campanha}')
def encerrar_campanha(nome_campanha: str):
    """
    Encerra qualquer tipo de campanha
    que tenha o nome igual ao procurado
    """
    excluidas = {}
    for campanha in Campanha.find_all(nome=nome_campanha):
        cls = campanha.__class__
        excluidas[cls.__name__] = cls.delete(
            nome=nome_campanha
        ).deleted_count
    if excluidas:
        return {
            'campanhas_excluidas': excluidas,
        }
    return 'Nenhuma campanha excluída.'
