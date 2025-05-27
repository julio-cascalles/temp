TEST_DATABASE = 'test'


class MongoTable:
    URL_HOST = 'mongodb://localhost:27017/'
    DATABASE_NAME = ''
    primary_key = ''
    class_type_field = 'class_type'
    _db = None

    @classmethod
    def table_name(cls) -> str:
        return cls.__name__

    @classmethod
    def collection(cls):
        if MongoTable._db is None:
            from pymongo import MongoClient
            conn = MongoClient(cls.URL_HOST, connect=False)
            if cls.DATABASE_NAME == TEST_DATABASE:
                conn.drop_database(cls.DATABASE_NAME)
            MongoTable._db = conn[cls.DATABASE_NAME]
        return MongoTable._db.get_collection(cls.table_name())

    def save(self):
        record  = {
            k: v for k, v in self.__dict__.items()
            if not k.startswith('_')
        }
        key = self.primary_key or list(record)[0]
        class_type = self.__class__.__name__
        if self.table_name() != class_type:
            record[self.class_type_field] = class_type
        self.collection().update_one(
            {key: record[key]},
            {'$set': record},
            upsert=True
        )

    @classmethod
    def find(cls, **args) -> list:
        SUB_CLASSES = {
            sub.__name__: sub for sub in cls.__subclasses__()
        }
        def create_obj(row: dict):
            class_type = cls
            if cls.class_type_field in row:
                class_type = SUB_CLASSES.get(
                    row[cls.class_type_field], cls
                )
            return class_type(**row)
        return [create_obj(o) for o in cls.collection().find(filter=args)]

    @classmethod
    def delete(cls, **args):
        return cls.collection().delete_many(args)
