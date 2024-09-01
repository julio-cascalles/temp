import re
from datetime import datetime
from dataclasses import dataclass
from dados import CONTRATOS

FORMATO_DATA = '%d/%m/%Y'
TAMANHO_DA_LINHA = 80

def periodo(dias: int) -> str:
    meses, _ = divmod(dias, 30)
    anos, meses = divmod(meses, 12)
    res = []
    if anos > 0:
        res.append('{} {}'.format(
            anos , 'ano' if anos == 1 else 'anos'
        ))
    if meses > 0:
        res.append('{} {}'.format(
            meses, 'mes' if meses == 1 else 'meses'
        ))
    if not res:
        res = [f'{dias} dias']
    return ' e '.join(res)


@dataclass
class Empresa:
    cnpj: str
    nome: str
    ini: datetime
    fim: datetime

    @property
    def tempo(self) -> int:
        return (self.fim - self.ini).days

    def __sub__(self, proxima) -> int:
        # Tempo depois de sair desta empresa e entrar na próxima:
        return (proxima.ini - self.fim).days


def maior_tempo_entre(empresas: list[Empresa]) -> str:
    maior = 0
    ultima = None
    res = ''
    for empresa in empresas:
        if ultima and ultima-empresa > maior:
            maior = ultima-empresa
            res = '{} entre {} e {}'.format(
                periodo(maior), ultima.nome, empresa.nome
            )
        ultima = empresa
    return res

def agrupado_por_tempo(empresas: list[Empresa]) -> dict:
    res = {}
    for empresa in empresas:
        res.setdefault(periodo(empresa.tempo), []).append(empresa.nome)
    return res

def mostra_total(empresas: list[Empresa]):
    total = sum(e.tempo for e in empresas)
    qtde = len(empresas)
    print('Total de tempo trabalhado:', periodo(total))
    print('Média de permanência no trabalho:', periodo(int(total/qtde)))
    print('Quantidade de empresas:', qtde)

def analise(descr: str, empresas: list[Empresa], detalhada: bool=False):
    print(descr.center(TAMANHO_DA_LINHA, '='))
    print('Empresa mais antiga:', min(empresas, key=lambda e: e.ini).nome)
    print('Empresa que ficou mais tempo: ', max(empresas, key=lambda e: e.tempo).nome)
    print('Maior tempo parado: ', maior_tempo_entre(empresas))
    mostra_total(empresas)
    if not detalhada:
        return
    print('Detalhes deste período:'.center(TAMANHO_DA_LINHA, '-'))
    empresas = sorted(empresas, key=lambda e: e.tempo) # --- ordena por tempo trabalhado
    for tempo, lista in agrupado_por_tempo(empresas).items():
        print(f'\t{tempo}:')
        for empresa in lista:
            print(f'\t\t{empresa}')


def todas_empresas():
    res = []
    for linha in CONTRATOS:
        cnpj, nome, ini, fim = [
            item for item in re.split(
            '^([0-9./-]+)|([0-9]+[/][0-9]+[/][0-9]+)', linha
            )
            if item and item.strip()
        ]
        empresa = Empresa(
            cnpj, nome, 
            datetime.strptime(ini, FORMATO_DATA),
            datetime.strptime(fim, FORMATO_DATA)
        )
        res.append(empresa)
    res.sort(key=lambda e: e.ini) # ---- ordena pelas empresas mais antigas
    return res

todas = todas_empresas()
antes_2004 = [e for e in todas if e.ini < datetime(2004, 1, 1)]
analise('Antes de 2004', antes_2004)
de2004_a2011 = [
    e for e in todas if 
    e.ini >= datetime(2004, 1, 1)
    and e.fim < datetime(2011, 1, 1)
]
analise('De 2004 a 2011', de2004_a2011)
depois_2011 = [e for e in todas if e.ini >= datetime(2011, 1, 1)]
analise('De 2011 em diante', depois_2011, detalhada=True)
print(' Total geral '.center(TAMANHO_DA_LINHA, '#'))
mostra_total(todas)
print('#'*TAMANHO_DA_LINHA)
