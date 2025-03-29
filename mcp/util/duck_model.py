from enum import Enum
from datetime import datetime
import duckdb
import re
from sql_blocks import Select, Where


class FileFormat(Enum):
    PARQUET = 'PARQUET'
    CSV = 'CSV'


class DuckModel:
    objects = {}
    primary_key = 'id'
    file_format: FileFormat = FileFormat.PARQUET
    to_display = set()
    debug: bool = True

    @classmethod
    def get_next_id(cls, **args):
        return len(cls.objects) + 1

    def __new__(cls, **args):
        if cls.primary_key not in args:
            args[cls.primary_key] = cls.get_next_id(**args)
        id = args[cls.primary_key]
        obj = cls.objects.get(id)
        if not obj:
            obj = super().__new__(cls)
            cls.objects[id] = obj
            schema = cls.schema()
            for key, value in args.items():
                ftype = schema.get(key)
                if ftype != datetime:
                    value = ftype(value)
                setattr(obj, key, value)
        return obj

    @classmethod
    def file_name(cls) -> str:
        return "{}.{}".format(
            cls.__name__, cls.file_format.value.lower()
        )

    @classmethod
    def schema(cls) -> dict:
        """
        Exemplo:
            {nome: str, idade: int, peso: float}
        """
        raise NotImplementedError('''
            Este método deve ser implementado
            nas classes-filhas.
        ''')
    
    @staticmethod
    def convert_field_type(class_type: type) -> str:
        VARCHAR_TYPE = 'varchar'
        if class_type.__base__ == Enum:
            return VARCHAR_TYPE
        return class_type.__name__.replace('str', VARCHAR_TYPE)

    @classmethod
    def find(cls, query:Select=None, **args) -> list['DuckModel']:
        if query:
            fields = [re.findall(r'\w+', f)[-1] for f in query.values['SELECT']]
        else:
            fields = cls.schema()
            query = Select( cls.file_name() )
            query.add_fields(fields)
        for key, value in args.items():
            cls.to_display.add(key)
            Where.eq(value).add(key, query)
        if not cls.to_display:
            cls.to_display = {cls.primary_key}
        if cls.debug:
            print('▒'*50)
            print(query)
            print('▒'*50)
        cur = duckdb.sql( str(query) )
        cls.objects = {}
        for values in cur.fetchall():
            data = {field: value for field, value in zip(fields, values)}
            cls(**data)
        return cls.objects.values()
    
    def get_values(self, field_set: set=None):
        for field, value in self.__dict__.items():
            if field_set and field not in field_set:
                continue
            if isinstance(value, Enum):
                yield value.value
            else:
                yield value

    @classmethod
    def save(cls):
        field_defs = cls.schema()
        con = duckdb.connect(database=':memory:')
        table_name = cls.__name__
        cmd = "CREATE TABLE {}({}\n);".format(
            table_name,
            ','.join( 
                f'\n\t{field} {DuckModel.convert_field_type(ftype)}'
                for field, ftype in field_defs.items() 
            )
        )
        con.execute(cmd)
        cmd = 'INSERT INTO {} VALUES ({})'.format(
            table_name, ','.join(['?'] * len(field_defs))
        )
        con.executemany(cmd, [
            list( obj.get_values() )
            for obj in cls.objects.values()
        ])
        con.execute("COPY {} TO '{}' (FORMAT {})".format(
            table_name, cls.file_name(), cls.file_format.value
        ))

    def __str__(self) -> str:
        return ' - '.join(
            str(val) for val in self.get_values(self.to_display)
        )

