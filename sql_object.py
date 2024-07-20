from enum import Enum

KEYWORD = {
    'SELECT': (',{}', 'SELECT *'),
    'FROM': ('{}', ''),
    'WHERE': ('{}AND ', ''),
    'GROUP BY': (',{} ', ''),
    'ORDER BY': (',{} ', ''),
    'LIMIT': (' ', ''),
}
SELECT, FROM, WHERE, GROUP_BY, ORDER_BY, LIMIT = KEYWORD.keys()


class SQLObject:
    def __init__(self, table_name: str=''):
        self.alias = ''
        self.values = {}
        self.key_field = ''
        self.set_table(table_name)
        self.linked_tables = {}

    def set_table(self, table_name: str):
        if not table_name:
            return
        if ' ' in table_name:
            table_name, self.alias = table_name.split()
        elif '_' in table_name:
            self.alias = ''.join(
                word[0].lower()
                for word in table_name.split('_')
            )
        else:
            self.alias = table_name.lower()[:3]
        self.values.setdefault(FROM, []).append(f'{table_name} {self.alias}')

    @property
    def table_name(self) -> str:
        return self.values[FROM][0].split()[0]
 

class Function:
    ...

class Field:
    prefix = ''

    @classmethod
    def format(cls, name: str, main: SQLObject) -> str:
        if name == '_':
            name = '*'
        else:
            name = f'{main.alias}.{name}'
        if Function in cls.__bases__:
            name = f'{cls.__name__}({name})'
        return f'{cls.prefix}{name}'

    @classmethod
    def add(cls, name: str, main: SQLObject):
        main.values.setdefault(SELECT, []).append(
            cls.format(name, main)
        )


class Avg(Function, Field):
    ...
class Min(Function, Field):
    ...
class Max(Function, Field):
    ...
class Sum(Function, Field):
    ...
class Count(Function, Field):
    ...

class Distinct(Field):
    prefix = 'DISTINCT '


class NamedField:
    def __init__(self, alias: str, class_type = Field):
        self.alias = alias
        if class_type not in [Field] + Field.__subclasses__():
            raise TypeError('class_type must be a Field (sub)class.')
        self.class_type = class_type

    def add(self, name: str, main: SQLObject):
        main.values.setdefault(SELECT, []).append(
            '{} as {}'.format(
                self.class_type.format(name, main),
                self.alias
            )
        )


class Table:
    def __init__(self, fields: list | str=[]):
        if isinstance(fields, str):
            fields = [f.strip() for f in fields.split(',')]
        self.fields = fields

    def add(self, name: str, main: SQLObject):
        main.set_table(name)
        for field in self.fields:
            Field.add(field, main)


class PrimaryKey:
    @staticmethod
    def add(name: str, main: SQLObject):
        main.key_field = name


class ForeignKey:
    def __init__(self, table_name: str):
        self.table_name = table_name

    def add(self, name: str, main: SQLObject):
        main.linked_tables[self.table_name] = name


class Where:
    def __init__(self, expr: str):
        self.expr = expr

    @classmethod
    def __constructor(cls, operator: str, value):
        if isinstance(value, str):
            return cls(expr=f"{operator} '{value}'")
        return cls(expr=f'{operator} {value}')

    @classmethod
    def eq(cls, value):
        return cls.__constructor('=', value)

    @classmethod
    def like(cls, value: str):
        return cls(f"LIKE '%{value}%'")
   
    @classmethod
    def gt(cls, value):
        return cls.__constructor('>', value)

    @classmethod
    def gte(cls, value):
        return cls.__constructor('>=', value)

    @classmethod
    def lt(cls, value):
        return cls.__constructor('<', value)

    @classmethod
    def lte(cls, value) -> str:
        return cls.__constructor('<=', value)

    def add(self, name: str, main: SQLObject):
        main.values.setdefault(WHERE, []).append('{} {}'.format(
            Field.format(name, main), self.expr
        ))


class Options:
    def __init__(self, **values):
        self.__children: dict = values

    def add(self, logical_separator: str, main: SQLObject):
        """
        `logical_separator` must be AND or OR
        """
        conditions: list[str] = []
        for field, child in self.__children.items():
            conditions.append(' {} {} '.format(
                Field.format(field, main), child.expr
            ))
        main.values.setdefault(WHERE, []).append(
            '(' + logical_separator.join(conditions) + ')'
        )


class SortType(Enum):
    ASC = ''
    DESC = ' DESC'

class OrderBy:
    sort: SortType = SortType.ASC
    @classmethod
    def add(cls, name: str, main: SQLObject):
        if main.alias:
            name = f'{main.alias}.{name}'
        main.values.setdefault(ORDER_BY, []).append(name + cls.sort.value)


class GroupBy:
    @staticmethod
    def add(name: str, main: SQLObject):
        main.values.setdefault(GROUP_BY, []).append(f'{main.alias}.{name}')


class Having:
    def __init__(self, function: Function, condition: Where):
        self.function = function
        self.condition = condition

    def add(self, name: str, main:SQLObject):
        main.values[GROUP_BY][-1] += ' HAVING {} {}'.format(
            self.function.format(name, main), self.condition.expr
        )
    
    @classmethod
    def avg(cls, condition: Where):
        return cls(Avg, condition)
    
    @classmethod
    def min(cls, condition: Where):
        return cls(Min, condition)
    
    @classmethod
    def max(cls, condition: Where):
        return cls(Max, condition)
    
    @classmethod
    def sum(cls, condition: Where):
        return cls(Sum, condition)
    
    @classmethod
    def count(cls, condition: Where):
        return cls(Count, condition)


class JoinType(Enum):
    INNER = ''
    LEFT = 'LEFT '
    RIGHT = 'RIGHT '
    FULL = 'FULL '

class Select(SQLObject):
    join_type: JoinType = JoinType.INNER

    def __init__(self, table_name: str='', **values):
        super().__init__(table_name)
        to_list = lambda x: x if isinstance(x, list) else [x]
        for name, params in values.items():
            for obj in to_list(params):
                obj.add(name, self)
        self.break_lines = True

    def add(self, name: str, main: SQLObject):
        def update_values(key: str, new_values: list):
            for value in new_values:
                old_values = main.values.get(key, [])
                if value not in old_values:
                    main.values[key] = old_values + [value]
        update_values(
            FROM, [
                '{0}JOIN {1} ON ({2}.{3} = {4}.{5})'.format(
                    self.join_type.value, # -------- {0}
                    self.table_name, # ------------- {1}
                    main.alias, name, # ------------ {2} {3}
                    self.alias, self.key_field # --- {4} {5} 
                )
            ] + self.values[FROM][1:]
        )
        for key in (SELECT, WHERE, ORDER_BY):
            update_values(key, self.values.get(key, []))

    def __add__(self, other: SQLObject):
        foreign_field = self.linked_tables.get(other.table_name)
        if not foreign_field:
            raise ValueError(f'No relationship found between {self.table_name} and {other.table_name}.')
        other.add(foreign_field, self)
        return self

    def __str__(self) -> str:
        TABULATION = '\n\t' if self.break_lines else ' '
        LINE_BREAK = '\n' if self.break_lines else ' '
        DEFAULT = lambda key: KEYWORD[key][1]
        FMT_SEP = lambda key: KEYWORD[key][0].format(TABULATION)
        select, _from, where, groupBy, orderBy, limit = [
            DEFAULT(key) if not self.values.get(key) else "{}{}{}{}".format(
                LINE_BREAK, key, TABULATION, FMT_SEP(key).join(self.values[key])
            ) for key in KEYWORD
        ]
        return f'{select}{_from}{where}{groupBy}{orderBy}{limit}'.strip()
   
    def __call__(self, **values):
        for name, obj in values.items():
            obj.add(name, self)
        return self
    
    def __eq__(self, other: SQLObject) -> bool:
        def sorted_values(obj: SQLObject, key: str) -> list:
            return sorted(obj.values.get(key, []))
        for key in KEYWORD:
            if sorted_values(self, key) != sorted_values(other, key):
                return False
        return True

    def limit(self, row_count: int, offset: int=0):
        result = [str(row_count)]
        if offset > 0:
            result.append(f'OFFSET {offset}')
        self.values.setdefault(LIMIT, result)
        return self


class SubSelect(Select):
    def add(self, name: str, main: SQLObject):
        self.break_lines = False
        Where(f'IN ({self})').add(name, main)



def test_varios_objetos() -> tuple:
    def select_ator() -> Select:
        return Select('Ator a', elenco=ForeignKey('Elenco'),
            nome=NamedField('nome_ator')
        )
    def select_elenco() -> Select:
        return Select(
            Elenco=Table('papel'), id=PrimaryKey, filme=ForeignKey('Filme'),
        )
    def melhores_filmes() -> SubSelect:
        return SubSelect( # ---- Filmes com boas críticas
            'Critica c',  filme=[GroupBy, Distinct], nota=Having.avg(Where.gt(4.5))
        )
    def select_filme() -> Select:
        return Select('Filme f', titulo=Field,
            lancamento=[OrderBy, Field], id=PrimaryKey,
            OR=Options(
                genero=Where.eq('Sci-Fi'), premios=Where.like('Oscar')
            )
        )
    return select_ator(), select_elenco(), melhores_filmes(), select_filme()

def teste_objeto_simples():
    return Select(
        'Ator a', nome=NamedField('nome_ator'),
        elenco=Select(
            Elenco=Table('papel'), id=PrimaryKey,
            filme=Select(
                'Filme f', titulo=Field,
                lancamento=[OrderBy, Field],
                id=[SubSelect(
                        'Critica c', filme=[GroupBy, Distinct],
                        nota=Having.avg(Where.gt(4.5))
                    ), PrimaryKey
                ], OR=Options(
                    genero=Where.eq('Sci-Fi'), premios=Where.like('Oscar')
                )
            ) # --- Filme
        ) # ------- Elenco
    ) # ----------- Ator


if __name__ == "__main__":
    Select.join_type = JoinType.LEFT
    OrderBy.sort = SortType.DESC
    a, e, m, f = test_varios_objetos()
    print('------- [1] melhores_filmes ------------------------------------')
    print(m)
    print('------- [2] ator + elenco --------------------------------------')
    print( a + e )
    print('------- [3] elenco + filme -------------------------------------')
    print( e + f )
    print('------- [4] filme( id=melhores_filmes ) ------------------------')
    f = f(id=m) # <<-- Coloca `melhores_filmes` como sub-query de `id`
                #       f.id IN (SELECT ...)
    print(e + f)
    print('------- [5] ator + elenco + filme ------------------------------')
    soma = a + (e + f)
    #          ^
    #          |
    #          +------  Elenco é somado com Filme ANTES de Ator,
    #                  porque Ator e Filme não tem relacionamento
    print(soma)
    print('------- [6] objeto_simples -------------------------------------')
    query = teste_objeto_simples()
    print(query)
    print('-------- objeto_simples == (ator + elenco + filme) ?? ----------')
    print('>'*20, 'Objetos iguais!' if query == soma else 'DIFERENTES...')
