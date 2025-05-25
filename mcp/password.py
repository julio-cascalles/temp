from mcp.server.fastmcp import FastMCP
from string import (
    ascii_lowercase,
    ascii_uppercase,
    digits,
    punctuation
)
from random import choice, shuffle


mcp = FastMCP("Password")



def get_rules(**args) -> list[tuple]:
    return [
        ( ascii_lowercase,   args.get('lowercase', 4) ),
        ( ascii_uppercase,   args.get('uppercase', 2) ),
        ( digits,            args.get('digits', 1) ),
        ( punctuation,       args.get('symbols', 1) ),
    ]

@mcp.tool()
def generate_password() -> str:
    """
    Gera uma nova senha, combinando letras
    minúsculas, maíuscula, dígito e símbolo.
    """
    rules = get_rules()
    char_list = [
        choice(source) for source, size in rules
        for _ in range(size)
    ]
    shuffle(char_list)
    return ''.join(char_list)

@mcp.tool()
def password_is_valid(text: str) -> bool:
    """
    Verifica se a senha obedece às regras:
    4 letras minúsculas;
    2 letras maiúsculas;
    1 dígito (0-9);
    1 caractere de símbolo.
    """
    rules = get_rules()
    for source, size in rules:
        for char in text:
            if char in source:
                size -= 1
        if size != 0:
            return False
    return True


if __name__ == '__main__':
    mcp.run()
