from modelos.util.sinalizador import Sinalizador


class Categoria(Sinalizador):
    ROUPA       =     1
    CALCADO     =     2 
    ACESSORIO   =     4 
    MASCULINA   =     8 
    FEMININA    =    16  
    INFANTIL    =    32  
    PRAIA       =    64
    FITNESS     =   128   
    RELAX       =   256
    INTIMA      =   512
    FRIO        =  1024

    @classmethod
    def item_enum(cls, name: str):
        return {
            'MASCULINO': cls.MASCULINA,
            'FEMININO': cls.FEMININA,
        }.get(name) or super().item_enum(name)


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