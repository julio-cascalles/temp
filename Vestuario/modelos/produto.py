from pydantic import BaseModel
from modelos.util.subcategorias import SubCategoria


class Produto(BaseModel):
    nome: str
    categoria: list[SubCategoria]
    valor: float
