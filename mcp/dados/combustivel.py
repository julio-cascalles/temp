from enum import Enum


class Combustivel(Enum):
    """
    Acentos removidos para facilitar a pesquisa
    """
    ALCOOL =   'Alcool' # "Álcool"
    GASOLINA = "Gasolina"
    DIESEL =   "Diesel"
    GNV =  'Gas' # "Gás"
    ELETRICO = 'Eletrico' # "Elétrico"
    HIBRIDO =  'Hibrido' # "Híbrido"
