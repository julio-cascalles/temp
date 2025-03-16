import re
"""
Baseado no desafio da LeetCode:
1071. Greatest Common Divisor of Strings
"""

def str_division(s: str, t: str) -> dict:
    def get_str_from_set(obj: set, source: str) -> str:
        chars = ''.join(obj)
        return ''.join( re.findall( fr"[{chars}]", source ))
    pattern = get_str_from_set(
        set(s).intersection(set(t)), t
    )
    found = re.findall(pattern, s)
    rest = get_str_from_set(
        set(s).difference(set(pattern)), s
    )
    return {
        'pattern': pattern,
        'count': len(found),
        'rest': rest,
    }


def main():
    import json
    s = input('String #1 (s): ')
    t = input('String #2 (t): ')
    print(
        json.dumps(str_division(s, t),indent=4)
    )

if __name__ == '__main__':
    main()

