class Habilidade:
    def __init__(self, nome: str, valor: float):
        self.nome, self.valor = nome, valor

class ElementoProcSeletivo:
    def __init__(self, habilidades: list[Habilidade]):
        self.habilidades = habilidades

class Vaga(ElementoProcSeletivo):
    def __init__(self, titulo: str, habilidades: list[Habilidade]):
        super().__init__(habilidades)
        self.salario, self.titulo = sum( h.valor for h in habilidades ), titulo

class Candidato(ElementoProcSeletivo):
    def compatibilidade(self, vaga: Vaga) -> float:
        s1, s2 = ( set(h.nome for h in obj.habilidades) for obj in [self, vaga])
        return len(s1.intersection(s2)) / len(vaga.habilidades) * 100
    

def anuncio(vaga: Vaga, candidato: Candidato) -> str:
    return '\nVaga: {}\n\nRequisitos:{}\nSalário:{:_.2f}\nCompatibilidade:{:.2f}%\n'.format(
        vaga.titulo, ','.join(h.nome for h in vaga.habilidades), 
        vaga.salario,  candidato.compatibilidade(vaga)
    )


PYTHON, SQL, DEJANGO = [ Habilidade(N, V) for N, V in (
    ('Python', 4500), ('SQL', 3700), ('Dejango', 1000)
) ]

if __name__ == '__main__':
    print('='*30, anuncio(
        Vaga('Analista Pleno', [PYTHON, SQL, DEJANGO]),
        Candidato([PYTHON, SQL])
    ), '-'*30)
