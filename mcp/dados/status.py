from enum import Enum

class Status(Enum):
    OK = "OK"
    PENDENCIA_DETRAN = "DETRAN"
    SINISTRO = "Sinistro" # já foi batido, roubado...
    FINANCEIRO = "Financeiro"
    # ^^--- Alienado ou com problemas financeiros
