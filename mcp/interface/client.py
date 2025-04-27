from mcp.server.fastmcp import FastMCP
from interface.server import Server


mcp = FastMCP("Consulta de veículos")


@mcp.tool()
def procurar_veiculo(
    marca: str='', modelo: str='', cor: str='',
    ano: int=0, km: float=0, combustivel: str=''
) -> str:
    """
    Envia filtros para o servidor e formato a resposta
    :
    """
    filtros = {campo: valor for campo, valor in locals().items() if valor}
    return '\n'.join( str(carro) for carro in Server(**filtros).data )
