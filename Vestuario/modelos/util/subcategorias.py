from enum import IntFlag, auto
import re


class SubCategoria(IntFlag):
    ROUPA = auto()
    CALCADO = auto()
    ACESSORIO = auto()
    MASCULINA = auto()
    FEMININA = auto()
    INFANTIL = auto()
    PRAIA = auto()
    FITNESS = auto()
    RELAX = auto()
    INTIMA = auto()
    FRIO = auto()

    @classmethod
    def combine(cls, expr: str) -> set:
        result = set()
        for name in re.split('[+,]', expr):
            catego = SubCategoria[name.strip()]
            result.add(catego)
        return result

"""
Exemplos:

pijama = ROUPA + RELAX
pantufa = CALCADO + RELAX

chinelo = CALCADO + RELAX + PRAIA

biquini = ROUPA + FEMININA + PRAIA
sunga = ROUPA + MASCULINA + PRAIA

cueca_infantil = (
    ROUPA + INTIMA + MASCULINA + INFANTIL
)

Legging = ROUPA + FEMININA + FITNESS
sapatilha_bailarina = CALCADO + FITNESS + FEMININO

gravata = ACESSORIO + MASCULINO
bolsa = ACESSORIO + FEMININO

blusa = ROUPA + FRIO
cachecol = ACESSORIO + FRIO

moletom = ROUPA + RELAX + FRIO
gorro_ursinho = ACESSORIO + FRIO + INFANTIL
"""