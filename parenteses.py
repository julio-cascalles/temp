import re

ABRIR =  '({['
FECHAR = ')}]'
SEPARADORES = '|'.join(f'\\{c}' for c in ABRIR + FECHAR)
ERR_FECHADO_COM_CH_INESPERADO = 1
ERR_PARENTESES_DESBALANCEADOS = 2


def erro_parenteses(texto: str) -> int:
    esperado: list = []
    for sep in re.findall(SEPARADORES, texto):
        if sep in ABRIR:
            pos = ABRIR.index(sep)
            esperado.append(FECHAR[pos])
        elif sep == esperado[-1]:
            esperado.pop(-1)
        else:
            return ERR_FECHADO_COM_CH_INESPERADO
    if esperado:
        return ERR_PARENTESES_DESBALANCEADOS
    return 0  # ----- Sucesso!


if __name__ == '__main__':
    assert not erro_parenteses("([]){}")
    assert erro_parenteses("([)]")  == ERR_FECHADO_COM_CH_INESPERADO
    assert erro_parenteses("((())") == ERR_PARENTESES_DESBALANCEADOS
    print('Passou em todos os testes!'.center(50, '*'))
