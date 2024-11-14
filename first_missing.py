from random import randint, choice, shuffle


def first_missing(arr: list, **args) -> int:
    """
    To-Do: O que fazer quando faltam VÁRIOS itens na lista?!?!?
    """
    a1 = args.get('a1') or min(arr)
    an = args.get('an') or max(arr)
    n = args.get('n') or len(arr)+1
    sn = (a1+an)*n/2
    return sn - sum(arr)

def get_arr() -> dict: # ....... Dados para teste ......
    a1 = randint(-100, 100)
    n = randint(5, 20)
    incr = choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
    an = a1+n*incr
    arr = [i for i in range(a1, an, incr)]
    an -= incr
    shuffle(arr)
    selected = choice(arr)
    arr.remove(selected)
    return locals()

if __name__ == '__main__':
    params = get_arr()
    print('-'*50)
    print(params)
    selected = params.pop('selected')
    assert selected == first_missing(**params)
    assert first_missing([1,2,3,5,6,7,8,9]) == 4
    print('Success!'.center(50, '='))
