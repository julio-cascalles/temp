import json
from datetime import datetime, timedelta


NUMERO_BANCO = {
    '001': 'Banco do Brasil', '033': 'Banco Santander Brasil',
    '077': 'Banco Inter', '104': 'Caixa Econômica Federal',
    '208': 'BTG Pactual', '237': 'Banco Bradesco',
    '260': 'Nubank', '290': 'Banco Pagseguro', '336': 'C6 Bank',
    '341': 'Banco Itaú', '655': 'Banco Votorantim'}

def data_bancaria(dias: int) -> str:
    dt_ref = datetime(day=7, month=10, year=1997) + timedelta(days=dias)
    return dt_ref.strftime('%d/%m/%Y')

CAMPOS_BOLETO = {
    'banco': (3, lambda x: [x, NUMERO_BANCO.get(x, '???')]),
    'moeda': (1, None), 'contrato': (11, None),
    'nosso_numero': (6, None), 'campo_livre': (11, None),
    'digito': (1, None),
    'vencimento': (4, lambda x: data_bancaria(int(x))),
    'valor': (10, lambda x: float(x) / 100),
}

def dados_boleto(cod_barras: str, campos: dict=CAMPOS_BOLETO) -> dict:
    cod_barras = ''.join(c for c in cod_barras if c.isdecimal())
    ini, fim = 0, 0
    resultado = {}
    for nome, (tam, func) in campos.items():
        fim = ini + tam
        conteudo = cod_barras[ini: fim]
        if func:
            conteudo = func(conteudo)
        resultado[nome] = conteudo
        ini = fim
    return resultado


if __name__ == '__main__':
    print(json.dumps(
        dados_boleto(cod_barras=input('Digite o códigod de barras: ')),
        indent=4
    ))






