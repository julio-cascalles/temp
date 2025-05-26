from enum import IntFlag, auto
import re

class Sinalizador(IntFlag):
    @classmethod
    def combo(cls, expr: str) -> set:
        result = set()
        for name in re.findall( r'\w+', expr.upper() ):
            result.add( cls[name.strip()] )
        return result
