from enum import IntFlag, auto
import re

class Sinalizador(IntFlag):

    @classmethod
    def item_enum(cls, name: str) -> 'IntFlag':
        return cls[name.strip()]

    @classmethod
    def combo(cls, expr: str) -> list:
        result = set()
        for name in re.findall( r'\w+', expr.upper() ):
            try:
                result.add( cls.item_enum(name) )
            except:
                continue
        return list(result)
