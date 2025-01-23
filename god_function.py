def faz_todos_os_cálculos_v1(compra):
    # ------- Cálculo de preço --------
    # ------- Cálculo de desconto -----
    if regra_promoção:
        desconto = ...
    if regra_fidelidade:
        desconto = ...
    if regra_grandes_quantidades:
        desconto = ...
    # ------- Cálculo de impostos -----
    ...
    # ------- Cálculo de frete --------
    ...
    # ------- Cálculo de lucro --------
    ...
    # ------- Cálculo de custos -------
    ...
    # >>>>>>>>>>> 500 linhas de código!!!!!!!!!!!!!!
    # 😱😱😱

class Regra:
    def aplica_desconto(self, compra):
        ...

def calculo_desconto(compra, regras: list[Regra]):
    for regra in regras:
        desconto = regra.aplica_desconto(compra)
        compra.preço *= (1 - desconto / 100)


def faz_todos_os_cálculos_v2(compra):
    calculo_preço(compra)
    calculo_desconto(compra, [
        RegraPromoção(),
        RegraFidelidade(),
        RegraGrandesQuantidades()
    ])
    calculo_impostos(compra)
    calculo_frete(compra)
    calculo_lucro(compra)
    calculo_custos(compra)

def calculo_preço(compra, novo_cálculo: bool=False):
    ...
    if novo_cálculo:
        # <<---- A sua alteração vai aqui!

def calculo_impostos(compra, novo_cálculo: bool=False):
    ...
    if novo_cálculo:
        # <<---- A sua alteração vai aqui!

def calculo_frete(compra, novo_cálculo: bool=False):
    ...
    if novo_cálculo:
        # <<---- A sua alteração vai aqui!

def calculo_lucro(compra, novo_cálculo: bool=False  ):
    ...
    if novo_cálculo:
        # <<---- A sua alteração vai aqui!

def calculo_custos(compra, novo_cálculo: bool=False):
    ...
    if novo_cálculo:
        # <<---- A sua alteração vai aqui!

