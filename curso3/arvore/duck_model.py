from datetime import datetime
import duckdb


class DuckModel:
    objects = {}
    primary_key = 'id'

    def __new__(cls, **args):
        id = args.get(cls.primary_key, 0)
        obj = cls.objects.get(id)
        if not obj:
            obj = super().__new__(cls)
            cls.objects[id] = obj
            for key, value in args.items():
                setattr(obj, key, value)
        return obj

    @classmethod
    def file_name(cls, suffix: str='') -> str:
        if not suffix:
            suffix = datetime.today().strftime('%Y%m%d')
        return "{}_{}.parquet".format(
            cls.__name__, suffix
        )

    @staticmethod
    def date_pattern(year: int=0, month:int = 0) -> str:
        if not year:
            if not month:
                return '*'
            else:
                return f'????{month:02d}'
        elif not month:
            return f'{year}*'
        return f'{year}{month:02d}'

    @staticmethod
    def connection():
        return duckdb.connect(database=':memory:')

    @classmethod
    def schema(cls) -> dict:
        sample = list( cls.objects.values() )[0]
        return {
            field: value.__class__.__name__.replace('str', 'varchar')
            for field, value in sample.__dict__.items()
        }

    @classmethod
    def find(cls, **args) -> dict:
        field_defs = cls.schema()
        year, month = (args.pop(key, 0) for key in ('year', 'month'))
        con = cls.connection()
        ref = cls.date_pattern(year, month)
        cur = con.execute("SELECT {} FROM '{}' WHERE {}".format(
            ','.join(field_defs), cls.file_name(ref), 
            ' AND '.join(f'{field} = ?' for field in args)
        ), args.values())
        cls.objects = {}
        for row in cur.fetchall():
            data = {field: value for field, value in zip(field_defs, row)}
            cls(**data)
        return cls.objects            

    @classmethod
    def save(cls):
        field_defs = cls.schema()
        con = cls.connection()
        table_name = cls.__name__
        con.execute("CREATE TABLE {}({});".format(
            table_name,
            ','.join( f'{field} {ftype}' for field, ftype in field_defs.items() )
        ))
        command = 'INSERT INTO {} VALUES ({})'.format(
            table_name, ','.join(['?'] * len(field_defs))
        )
        con.executemany(command, [
            obj.__dict__.values() for obj in cls.objects.values()
        ])
        con.execute("COPY {} TO '{}' (FORMAT PARQUET)".format(
            table_name, cls.file_name()
        ))


if __name__ == "__main__":
    pass