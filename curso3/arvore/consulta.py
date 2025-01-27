import duckdb
from datetime import datetime
from duck_model import DuckModel
from sql_blocks import Select, Recursive, Where


class Pessoa(DuckModel):
    objects = {}

    @classmethod
    def file_name(cls, suffix: str='') -> str:
        return 'Pessoas.parquet'

    @classmethod
    def schema(cls) -> dict:
        return {
            'id': 'int',
            'nome': 'varchar',
            'sobrenome': 'varchar',
            'pai': 'int',
            'mae': 'int',
            'nascimento': 'datetime',
        }


def cte(id: int):
    def get_query(i: int):
        query = Select(f"{Pessoa.file_name()} p{i}")
        query.add_fields( Pessoa.schema() )
        return query
    q1, q2 = [get_query(i) for i in (1, 2)]
    q1(id=Where.eq(id))
    q2(
        id=Where.formula('(% = a.pai OR % = a.mae)')
    )        
    result = str( Recursive('ancestrais', [q1, q2]) )
    print('-'*50)
    print(result)
    print('-'*50)
    return duckdb.sql(result)

def monta_arvore(id: int, nível: int = 0):
    if nível == 0:
        cursor = cte(id)
        for row in cursor.fetchall():
            dados = {field: row[i] for i, field in enumerate(Pessoa.schema())}
            Pessoa(**dados)
    pessoa = Pessoa.objects[id]
    sep = '    ' * nível
    linha = f'{sep}{pessoa.nome} {pessoa.sobrenome}'
    linha += datetime.strftime(pessoa.nascimento, '%d/%m/%Y').rjust(60-len(linha), '.')
    linha += f'({pessoa.id})'.rjust(10, ' ')
    print(linha)
    if pessoa.pai:
        monta_arvore(pessoa.pai, nível + 1)
    if pessoa.mae:
        monta_arvore(pessoa.mae, nível + 1)


if __name__ == "__main__":
    monta_arvore(32630)


"""
Sophie Barbosa Teixeira...........................28/12/2020   (32630)
    Bruno Moura Teixeira..........................06/06/2000    (2402)
        Emanuel Fernandes Teixeira................28/08/1980    (2394)
            Vitor Gomes Fernandes.................09/09/1960      (49)
                Anthony Gabriel Fernandes.........18/05/1940      (47)
                Allana Gomes......................25/12/1940      (20)
            Isabelly Barbosa Teixeira.............21/03/1960     (104)
                Arthur Gabriel Teixeira...........25/07/1940      (41)
                Isis Barbosa......................06/04/1940      (44)
        Larissa Lima Moura........................14/03/1980    (1020)
            Isaac Mota Lima.......................06/09/1960     (276)
                Otávio Lima.......................14/12/1940      (15)
                Maitê Mota........................27/06/1940      (24)
            Agatha Almeida Moura..................17/02/1960     (201)
                Henry Gabriel Almeida.............19/10/1940      (27)
                Juliana Moura.....................18/07/1940      (26)
    Larissa Fernandes Barbosa.....................07/07/2000    (3084)
        Benjamim Mota Barbosa.....................04/11/1980    (2173)
            Luiz Otávio Sousa Barbosa.............20/02/1960      (81)
                Calebe Barbosa....................23/12/1940      (43)
                Joana Sousa.......................09/09/1940       (6)
            Yasmin Gonçalves Mota.................26/07/1960     (228)
                Luiz Felipe Mota..................05/02/1940      (23)
                Vitória Gonçalves.................22/09/1940      (32)
        Maria Cecília Rodrigues Fernandes.........10/01/1980     (728)
            Enrico Nunes Fernandes................01/05/1960     (321)
                Henrique Nunes....................11/07/1940       (9)
                Marina Fernandes..................28/04/1940      (48)
            Isis Santos Rodrigues.................16/07/1960     (185)
                Levi Rodrigues....................07/03/1940      (29)
                Maria Santos......................25/10/1940      (18)
"""