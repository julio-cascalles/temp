TEST_DATABASE = 'test'

class MongoTable:
    URL_HOST = 'mongodb://localhost:27017/'
    DATABASE_NAME = ''
    _db = None

    @classmethod
    def collection(cls):
        if MongoTable._db is None:
            from pymongo import MongoClient
            conn = MongoClient(cls.URL_HOST, connect=False)
            if cls.DATABASE_NAME == TEST_DATABASE:
                conn.drop_database(cls.DATABASE_NAME)
            MongoTable._db = conn[cls.DATABASE_NAME]
        return MongoTable._db.get_collection(cls.__name__)

    def save(self, key_field_index: int = 0):
        record  = {
            k: v for k, v in self.__dict__.items()
            if not k.startswith('_')
        }
        key = list(record.keys())[key_field_index]
        self.collection().update_one(
            {key: record[key]},
            {'$set': record},
            upsert=True
        )

    @classmethod
    def find(cls, **args) -> list:
        return [cls(**o) for o in cls.collection().find(filter=args)]

    @classmethod
    def find_first(cls, **args):
        rows = [cls(**o) for o in cls.collection().find(filter=args).limit(-1)]
        # rows = [cls(**o) for o in cls.collection().find_one(filter=args)]
        return next(iter(rows), None)

    @classmethod
    def delete(cls, **args):
        return cls.collection().delete_many(args)
