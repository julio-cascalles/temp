import re
from enum import IntFlag
from string import (
    ascii_lowercase,
    ascii_uppercase,
    punctuation
)
from random import sample, shuffle


class Permissao(IntFlag):
    get_midias     =    1
    get_categorias =    2
    get_produtos   =    4
    get_clientes   =    8
    get_campanhas  =   16
    post_produto   =   32
    post_cliente   =   64
    lancamento     =  128
    liquidacao     =  256
    prospeccao     =  512
    del_campanha   = 1024
    admin_senhas   = 2048

    @classmethod
    def permissoes_da_senha(cls, senha: str) -> 'Permissao':
        nivel_acesso = int( ''.join(re.findall(r'\d+', senha)) )
        return Permissao(nivel_acesso)

    @classmethod
    def cria_senha(cls, nivel_acesso: int|list['Permissao']) -> str:
        if isinstance(nivel_acesso, list):
            nivel_acesso = sum(nivel_acesso)
        digitos = list( str(nivel_acesso).zfill(4) )
        caracteres = (
            sample(ascii_lowercase, 4) +
            sample(ascii_uppercase, 2) +
            sample(punctuation, 2)
        )
        shuffle(caracteres)
        intercalados = zip(
            caracteres[::2],
            digitos,
            caracteres[1::2],
        )
        return ''.join(f'{a}{num}{b}' for a, num, b in intercalados)
