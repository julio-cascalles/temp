# ---- Funções de Rastreamento: -----------
def exibe_cada_mes(mes: int, total: float):
    print(f'Mês {mes}: {total:_.2f}')

def funcao_vazia(mes: int, total: float):
    ...
# -----------------------------------------

def juntar(**args) -> dict:
    inicial = args.get('inicial', 0)
    investimento = args.get('investimento', 500)
    juros = args.get('juros', 0.5) / 100
    objetivo = args.get('objetivo', 0)
    prazo    = args.get('prazo', 0) # ----- quantidade de MESES !
    rendimento  = args.get('rendimento', 0)
    func_rastrear = args.get('func_rastrear', funcao_vazia)
    if all([not var for var in (objetivo, prazo, rendimento)]):
        raise Exception('É preciso informar um objetivo ou prazo ou valor rendimento.')
    total = inicial
    mes = 0
    sucesso = False
    while not sucesso:
        remuneração = total * juros
        total += (investimento + remuneração)
        mes += 1
        venceu_o_prazo = (mes == prazo)
        atingiu_objetivo = (objetivo != 0 and total >= objetivo)
        rendeu_bem = (rendimento != 0 and remuneração >= rendimento)
        sucesso = any([
            venceu_o_prazo, atingiu_objetivo, rendeu_bem
        ])
        func_rastrear(mes, total)
    anos, meses = divmod(mes, 12)
    return dict(
        total=total, 
        tempo=dict(anos=anos, meses=meses),        
        venceu_o_prazo=venceu_o_prazo,
        atingiu_objetivo=atingiu_objetivo,
        rendeu_bem=rendeu_bem,
        rendimento=remuneração,
    )


if __name__ == "__main__":
    import json
    from math import isclose
    TESTES = [
        (
            "Quanto eu teria se juntasse 250 por 20 anos?", dict(
                prazo=240,  investimento=250,
                func_rastrear=exibe_cada_mes,
            ), lambda res: isclose(res['total'], 115_510.224, rel_tol=1e-3)
        ),
        (
            "Em quantos anos eu juntaria 1 milhão?", dict(objetivo=1_000_000),
            lambda res: res['tempo']['anos'] == 40
        ),
        (
            "A partir de qual total eu tenho rendimento de R$ 3000,00 ?",
            dict(rendimento=3000),
            lambda res: isclose(res['total'], 606_474.04, rel_tol=1e-3)
        ),
        (
            "Eu tenho 110 mil. Consigo 445 mil em menos de 11 anos e com 1% a.m.?", dict(
                objetivo=445_000,
                juros=1, #  --- 1 % ao mês
                inicial=110_000,
                prazo=131, #   11 anos - 1 mês
            ),
            lambda res: res['atingiu_objetivo'] 
        ),
    ]
    json.encoder.c_make_encoder = None
    json.encoder.FLOAT_REPR = lambda o: format(o, '_.2f')
    for titulo, args, check_func in TESTES:
        res = juntar(**args)
        print('-'*50)
        print(titulo)
        print(json.dumps(res, indent=4, ))
        assert check_func(res)
    print('Passou em todos os testes!!'.center(50, '*'))
