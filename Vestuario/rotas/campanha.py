from fastapi import APIRouter, Depends, HTTPException, status
from modelos.campanha import Campanha, Lancamento, Liquidacao, Prospeccao
from modelos.util.categorias import Categoria
from modelos.util.midias import Midia
from modelos.cliente import Cliente


router = APIRouter()


def verifica_duplicada(campanha: Campanha):
    if Campanha.find(nome=campanha.nome):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe uma campanha com este nome."
        )

# ------- Grava por tipo de Campanha: ------------
@router.post('/campanha/lancamento')
def lancamento(campanha: Lancamento):
    verifica_duplicada(campanha)
    campanha.save()

@router.post('/campanha/liquidacao')
def liquidacao(campanha: Liquidacao):
    verifica_duplicada(campanha)
    campanha.save()

@router.post('/campanha/prospeccao')
def prospeccao(campanha: Prospeccao):
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
    return Campanha.find(**query)


@router.delete('/encerrar_campanha/{nome_campanha}')
def encerrar_campanha(nome_campanha: str):
    excluidas = {}
    for campanha in Campanha.find(nome=nome_campanha):
        cls = campanha.__class__
        excluidas[cls.__name__] = cls.delete(
            nome=nome_campanha
        ).deleted_count
    if excluidas:
        return {
            'campanhas_excluidas': excluidas,
        }
    return 'Nenhuma campanha excluída.'
