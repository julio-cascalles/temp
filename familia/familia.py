PAIS   = 'pais' 
FILHOS = 'filhos'
IRMAOS = 'irmãos'


class Pessoa:
    contador: int = 0

    def __init__(self, nome: str, pai: 'Pessoa'=None, mae: 'Pessoa'=None):
        Pessoa.contador += 1
        self.id = self.contador
        self.nome = nome
        self.parentesco = {}
        if not pai or not mae:
            return
        self.__relaciona(PAIS, FILHOS, {pai, mae})

    def grupo(self, tipo: str) -> set:
        return self.parentesco.get(tipo, set())

    def __relaciona(self, de: str, para: str, grupo: set):
        pessoa: 'Pessoa'
        for pessoa in grupo:
            self.parentesco.setdefault(de, set()).add(pessoa)
            if de == PAIS:
                self.__relaciona( 'avós', 'netos', pessoa.grupo(PAIS) )
                self.__relaciona( 'tios', 'sobrinhos', pessoa.grupo(IRMAOS) )
                self.__relaciona( IRMAOS, IRMAOS, pessoa.grupo(FILHOS) )
            pessoa.parentesco.setdefault(para, set()).add(self)

    def __str__(self) -> str:
        return """
        INSERT INTO Pessoa(id, nome) VALUES ({}, '{}');
        INSERT INTO Familia(pessoa1, pessoa2, parentesco)
        VALUES {}
        ;
        """.format(
            self.id, self.nome,
            ','.join(
                f"\n\t\t({self.id}, {pessoa.id}, '{tipo}') \t/* {pessoa.nome} */"
                for tipo, grupo in self.parentesco.items()
                for pessoa in grupo
            )
        )
        
    @classmethod
    def familia(cls, pai: 'Pessoa', mae: 'Pessoa', nomes: str) -> list:
        return [ cls(nome, pai, mae) for nome in nomes.split() ]

    @staticmethod
    def teste() -> list:
        # ---- Joao + Maria ---------------
        Joao  = Pessoa('Joao')
        Maria = Pessoa('Maria')
        Roberto, Sofia = Pessoa.familia(
            Joao, Maria, 'Roberto Sofia'
        )
        # ---- Pedro + Tereza ----------------
        Pedro  = Pessoa('Pedro')
        Tereza = Pessoa('Tereza')
        Guilherme, Manoela = Pessoa.familia(
            Pedro, Tereza, 'Guilherme Manoela'
        )
        return [
            Pessoa('Camila', Roberto, Manoela),
            Pessoa('Zelia', Guilherme, Sofia),
            Roberto, Manoela,
            Guilherme, Sofia,
        ]


if __name__ == "__main__":
    for pessoa in Pessoa.teste():
        print(pessoa)
        print('-'*50)

