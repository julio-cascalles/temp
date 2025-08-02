import re
from datetime import date, timedelta
from dateutil.easter import easter


class ExpressaoDeTempo:
    HOJE = None
    UNIDADES_TEMPO = {
        'dias': 1, 'semana': 7, 'semanas': 7,
        'mês': 30,'mes': 30, 'meses': 30, 'ano': 365, 'anos': 365
    }

    @staticmethod
    def numero_do_mes(mes: str) -> int:
        MESES = (
            'janeiro','fevereiro',  'março',
            'abril',  'maio',       'junho',
            'julho',  'agosto',  'setembro',
            'outubro','novembro','dezembro'
        )
        for i, nome in enumerate(MESES, 1):
            if nome == mes or mes == nome[:3]:
                return i
        return -1
    
    def dia_da_semana(self, dia: str) -> int:
        DIAS_SEMANA = (
            'segunda', 'terça', 'quarta',
            'quinta', 'sexta', 'sábado', 'domingo'
        )
        if dia not in DIAS_SEMANA:
            return -1
        return DIAS_SEMANA.index(dia)

    def data_fixa(self, txt: str) -> date:
        separadores = r'(\s+de\s+|[-/])'
        por_extenso = re.findall(fr'(\d+){separadores}(\w+|\d+){separadores}*(\d+)*', txt)
        if por_extenso:
            dia, _, mes, _, ano =  por_extenso[0]
            if not ano:
                ano = self.HOJE.year
            if mes.isalpha():
                mes = self.numero_do_mes(mes)
                if mes == -1:
                    return None
            return date( int(ano), int(mes), int(dia) )
        return None
    
    def data_por_nome(self, txt: str) -> date:
        EXPRESSOES_DE_DATA =  {
            "hoje":   self.HOJE,
            "ontem":  self.HOJE - timedelta(days=1),
            "amanhã": self.HOJE + timedelta(days=1)
        }
        if txt in EXPRESSOES_DE_DATA:
            return EXPRESSOES_DE_DATA[txt]
        return None
    
    def data_relativa(self, txt: str) -> date:
        BUSCAS = (r'em (\d+) (\w+)', r'(\d+) (\w+) atrás')
        for i, regex in enumerate(BUSCAS):
            encontrado = re.findall(regex, txt)
            if encontrado:
                num, unidade = encontrado[0]
                if i == 1: 
                    num = f'-{num}' # número negativo
                break
        if not encontrado or unidade not in self.UNIDADES_TEMPO:
            return None
        return self.HOJE + timedelta(
            days=self.UNIDADES_TEMPO[unidade] * int(num)
        )
    
    @staticmethod
    def expr_referencial(conteudo: str=r'\w+') -> list:
        return [
            fr'pr[óo]xim[ao]\s+({conteudo})', fr'({conteudo})\s+que vem',
            fr'({conteudo})\s+passad[ao]', fr'[úu]ltim[oa]\s+({conteudo})',
        ]
    
    def data_aproximada(self, txt: str) -> date:
        POS_NEGATIVA = 2
        for i, regex in enumerate(self.expr_referencial()):
            encontrado = re.findall(regex, txt)
            if not encontrado:
                continue
            unidade = encontrado[0]
            num = -1 if i >= POS_NEGATIVA else 1
            if unidade not in self.UNIDADES_TEMPO:
                dia_procurado = self.dia_da_semana(unidade)
                if dia_procurado == -1:
                    return None
                resultado = self.HOJE + timedelta(days=num)
                while resultado.weekday() != dia_procurado:
                    resultado += timedelta(days=num)
                return resultado
            break
        if not encontrado:
            return None
        return self.HOJE + timedelta(
            days=self.UNIDADES_TEMPO[unidade] * num
        )
    
    def data_apenas_dia(self, txt: str) -> date:
        encontrado = re.findall(r'dia (\d+)$', txt)
        if not encontrado:
            return None
        dia = encontrado[0]
        return self.HOJE.replace(day=int(dia))
    
    def carnaval(self, ano: int) -> date:
        return easter(ano) - timedelta(days=47)
    
    def natal(self, ano: int) -> date:
        return date(ano, 12, 25)
    
    def data_feriado(self, txt: str) -> date:
        POS_NEGATIVA = 2
        FUNC_FERIADO = {
            'natal': self.natal, 'carnaval': self.carnaval
        }
        BUSCAS = self.expr_referencial( '|'.join(FUNC_FERIADO) )
        resultado = None
        for i, regex in enumerate(BUSCAS):
            encontrado = re.findall(regex, txt)
            if not encontrado or (nome_feriado := encontrado[0]) not in FUNC_FERIADO:
                continue
            func = FUNC_FERIADO[nome_feriado]
            resultado = func(self.HOJE.year)
            if i >= POS_NEGATIVA and self.HOJE < resultado:
                resultado = func(self.HOJE.year - 1)
            elif self.HOJE > resultado:
                resultado = func(self.HOJE.year + 1)
        return resultado
    
    def __init__(self, txt: str):
        txt = txt.lower().strip()
        if not self.HOJE:
            self.HOJE = date.today()
        data = None
        METODOS = (
            self.data_fixa, self.data_por_nome,
            self.data_relativa, self.data_aproximada,
            self.data_apenas_dia, self.data_feriado,
        )
        for func in METODOS:
            data = func(txt)
            if data:
                break
        self.data = data


if __name__ == "__main__":
    TESTES = [
        ('16/7/2023',               '2023-07-16'),
        ('hoje',                    '2025-09-01'),
        ('ontem',                   '2025-08-31'),
        ('amanhã',                  '2025-09-02'),
        ('em 3 dias',               '2025-09-04'),
        ('2 semanas atrás',         '2025-08-18'),
        ('25 de novembro de 2024',  '2024-11-25'),
        ('25 de novembro',          '2025-11-25'),
        ('dia 14',                  '2025-09-14'),
        ('25/nov',                  '2025-11-25'),
        ('próxima semana',          '2025-09-08'),
        ('mês passado',             '2025-08-02'),
        ('ano passado',             '2024-09-01'),
        ('segunda passada',         '2025-08-25'),
        ('última terça',            '2025-08-26'),
        ('próxima quarta',          '2025-09-03'),
        ('quinta que vem',          '2025-09-04'),
        ('último natal',            '2024-12-25'),
        ('próximo carnaval',        '2026-02-17'),
    ]
    ExpressaoDeTempo.HOJE = date(2025, 9, 1)
    print('-'*50)
    for texto, esperado in TESTES:
        resultado = ExpressaoDeTempo(texto).data
        assert str(resultado) == esperado
        print(f'{texto:>30} = {resultado}')
    print('='*50)
    print('PASSOU EM TODOS OS TESTES!'.center(50, '*'))
