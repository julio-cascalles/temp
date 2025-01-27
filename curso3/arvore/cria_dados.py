from datetime import datetime
from faker import Faker
from dataclasses import dataclass
from random import randint, choice, shuffle
from duck_model import DuckModel


fake = Faker('pt_BR')


class Pessoa(DuckModel):
    objects = {}


NOMES_POR_GÊNERO = {  # Funções para nomes masculinos e femininos
    'M': fake.first_name_male,
    'F': fake.first_name_female,
}


@dataclass
class Familia:
    sobrenome: str
    pai: Pessoa
    mãe: Pessoa


def gera_filhos(familia: Familia, sexos: str) -> list[Pessoa]:
    filhos = []
    pai, mãe = familia.pai, familia.mãe
    if pai and mãe:
        novo_sobrenome = ' '.join( set(
            pessoa.sobrenome.split()[-1]
            for pessoa in (pai, mãe)
        ) )
        familia.sobrenome = novo_sobrenome
        decada = pai.nascimento.year + 20
    else:
        decada = 1940
    for sexo in sexos:
        func_nome = NOMES_POR_GÊNERO[sexo]
        pessoa=Pessoa(
            id=len(Pessoa.objects) + 1,
            nome=func_nome().split('.')[-1],
            sobrenome=familia.sobrenome,  sexo=sexo,
            pai=pai.id if pai else 0,
            mae=mãe.id if mãe else 0,            
            nascimento=datetime(decada, randint(1, 12), randint(1, 28))
        )
        filhos.append(pessoa)
    return filhos


SOBRENOMES = [
    "Sousa",     "Barbosa", "Freitas",   "Moura",
    "Lima",      "Silva",   "Fernandes", "Nunes",
    "Almeida",   "Mota",    "Oliveira",  "Pinto", 
    "Gomes",     "Santos",  "Teixeira",  "Mendes", 
    "Costa",     "Vieira",  "Ribeiro",   "Carvalho", 
    "Rodrigues", "Pereira", "Gonçalves", "Rocha",
]
shuffle(SOBRENOMES)

def cria_familias():
    for geração in range(1, 5):
        if geração == 1:
            homens, mulheres = [], []
            """
            Um homem e uma mulher de cada família:
            """
            for sobrenome in SOBRENOMES:
                homens += gera_filhos( Familia(sobrenome, None, None), 'M' )
                mulheres += gera_filhos( Familia(sobrenome, None, None), 'F' )
        filhos, filhas = [], []
        print(f'Geração {geração}: {len(homens)} casais.')
        qtd_filhos = abs(randint(6, 9) - geração) # --- Cada geração tem menos filhos
        while homens:
            homem = homens.pop()
            disponiveis = [mulher for mulher in mulheres if mulher.sobrenome != homem.sobrenome]
            if not disponiveis:
                continue
            mulher = choice(disponiveis)
            mulheres.remove(mulher)
            familia = Familia('', homem, mulher)
            filhos += gera_filhos(
                familia, ['M'] * qtd_filhos
            )
            filhas += gera_filhos(
                familia, ['F'] * qtd_filhos
            )
        homens = filhos
        mulheres = filhas
    print('\n Gravando dados...')
    Pessoa.save()
    print('PROCESSO CONCLUÍDO'.center(50, '*'))


if __name__ == "__main__":
    cria_familias()
