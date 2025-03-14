def find_unique(arr: list) -> int:
    i = len(arr)
    last = None
    while arr:
        i -= 1
        item = arr.pop()
        if item not in (None, last): # -- ignora duplicados e nulos
            if item not in arr:
                return i
            if last in arr:
                """
                Não deveria passar por aqui porque o enunciado
                fala em números repetidos em sequência, mas se
                ocorrer esta anamolia, este parece ser o único
                jeito:
                """
                arr = [None if x == last else x for x in arr]
        last = item
    return -1 # ---- Não encontrado!

def single_number(arr: list) -> int:
    """
    Esta é a função sugerida (por youtubers, no Medium,
    no StackOverflow...) para resolver ESPECIFICAMENTE
    o problema do LeetCode, mas FALHA quando testada 
    com outras variantes...❌
    """
    once = twice = 0
    for num in arr:
        once = ~twice & (once ^ num)
        twice = ~once & (twice ^ num)
    return once


if __name__ == "__main__":
    NUMBERS = [
        4,4,5,5,1,1,1,7,4,3,5,2,1,9,4,4,4,7,4,6,3,2,2,4,6,7,5,1,1,8,8
    ]
    CASES = [
        (13, find_unique),
        (9, single_number)
    ]
    for expected, func in CASES:
        print(f"Testing {func.__name__}...", end='')
        res = func(NUMBERS)
        if expected != res:
            print(f"ERROR: expected {expected} but got {res}")
        assert expected == res
        print('...Ok!')
    print('SUCCESS!'.center(50, '*'))
