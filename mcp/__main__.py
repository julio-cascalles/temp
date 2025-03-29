from interface import client, server, dados


OPCOES = {
    1: (
        "Iniciar servidor;", server.executa
    ),
    2: (
        "Criar banco de dados;", dados.executa
    ),
    3: (
        "Enviar consulta para o servidor.",
        client.executa
    ),
}
PROMPT = "Digite o número da opção desejada: "



def menu() -> int:
    print("""
        **** Agente virtual - Desafio Técnico C2S ****
        Em que posso ajudar? \n{}
        ----------------------------------------------
    """.format(
        '\n'.join(
            f"\t{num} - {txt}"
            for num, (txt, _) in OPCOES.items()
        )
    ))
    escolha = None
    while not escolha:
        try:
            opcao = int( input(PROMPT) )
        except ValueError:
            print('>> A opção deve ser um número entre {} e {}.'.format(
                min(OPCOES), max(OPCOES)
            ))
        escolha = OPCOES.get(opcao)
    func = escolha[1]
    func()

menu()
