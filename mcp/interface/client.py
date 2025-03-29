from dados.veiculo import Veiculo
from enum import Enum
from rotas.client import read_mcp


def valida(campo: str, valor: str) -> bool:
    schema = Veiculo.schema()
    if campo not in schema:
        print(f"\t O campo {campo} não existe na tabela `Veiculo`.") 
        return False
    try:
        schema[campo](valor)
    except:
        if schema[campo].__base__ ==  Enum:
            print('Valores possíveis para o campo {} são: \n{}'.format(
                campo, '\n'.join(item.value for item in schema[campo])
            ))
        else:
            print(f"\t O valor {valor} não é do tipo esperado para o campo {campo}.")            
        return False
    return True

def obtem_consulta() -> str:
    texto_digitado = input("Digite a consulta: ")
    return {
        key: value 
        for key, value in (param.split('=')
        for param in texto_digitado.split())
        if valida(key, value)
    }

def executa():
    print("""
        Exemplo de consulta:
          
            * marca=Honda
            * modelo=Fit
            * cor=azul
        > Combinação de filtros:
            marca=Honda modelo=Fit cor=azul
    """)
    resposta = ''
    while resposta.lower() != 's':
        consulta = obtem_consulta()
        print('*Confirme sua consulta antes de enviar:*')
        print(consulta)
        print('-' * 50)
        resposta = input("Deseja enviar a consulta? (s/n): ")
    print("Enviando consulta...")
    resultado = read_mcp(consulta)
    print('-' * 50)
    print("Resultado da consulta:")
    for item in resultado:
        print(item)
    print('-' * 50)
