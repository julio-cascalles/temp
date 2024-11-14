class Hora:
    def __new__(cls, param):
        if isinstance(param, str):
            valor = sum(
                int(s)*m for s, m in zip(
                    param.split(':'), [60, 1])
                    #     ^^            ^^-- m => valor de cada parte em min.
                    #      |
                    #      +--- s => cada parte da expressão (hora:minutos)
                )
        elif isinstance(param, int):
            valor = param
        else:
            return param
        obj = super().__new__(cls)
        obj.valor = valor
        return obj

    def __str__(self) -> str:
        minutos = self.valor % 60
        horas = ((self.valor - minutos) // 60) % 24
        return f'{horas}:{minutos:02d}'
    
    def __add__(self, hora):
        return Hora(self.valor + Hora(hora).valor)

    def __sub__(self, hora):
        return Hora(self.valor - Hora(hora).valor)

# ------------------------------------------------------------
if __name__ == "__main__":
    """
    Você pode somar...
        Hora + int
        Hora + str
        Hora + Hora
    """
    DUAS_E_MEIA = Hora('2:30')
    assert str(DUAS_E_MEIA + 45) == '3:15'
    assert str(DUAS_E_MEIA + '22:24') == '0:54'
    assert str(DUAS_E_MEIA + DUAS_E_MEIA) ==  '5:00'
    entrada, saida = Hora('10:53'), Hora('12:49')
    print('Fulano trabalhou das {} às {}. O que equivale a {}.'.format(
        entrada, saida, saida-entrada  
    )) # ==>> Fulano trabalhou das 10:53 às 12:49. O que equivale a 1:56.
