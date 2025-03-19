def longest_palindromes(s: str) -> str:
        if s == s[::-1]:
             return s
        map = {}
        result = s[0] if s else ''
        for i in range(len(s)):
            if len(s) > 100:
                p = s[:i+1]
                if s == p * (len(s) // len(p)):
                    return longest_palindromes(p)
            for x in map.get(s[i], []):
                y = i
                candidate = s[x:y+1]
                found = True
                while x < y:
                    if s[x] != s[y]:
                        found = False
                        break
                    x += 1
                    y -= 1
                if found and len(candidate) > len(result):
                    result = candidate
            map.setdefault(s[i], []).append(i)
        return result


def main():
    import re
    from unicodedata import normalize
    # =================================================================
    HUGE_STR = 'hanah'*400 # len = 2000
    CASES = [
        # ----- (1)  --------------------------------
        ('a', 'a'),  
        # ----- (2)  --------------------------------
        ('ac', 'a'),
        # ----- (3)  --------------------------------
        (HUGE_STR, HUGE_STR),
        # ----- (4)  --------------------------------
        ('Getulio, subi no ônibus em Marrocos.', 'subinoonibus'),
        # ----- (5)  --------------------------------
        ('Cuidado: A base do teto desaba.', 'abasedotetodesaba'),
        # ----- (6)  --------------------------------
        ('Ame o poema, apesar de tudo!', 'ameopoema'),
        # ----- (7)  --------------------------------
        ('Fique tranquilo: Anotaram a data da maratona. É amanhã.', 'anotaramadatadamaratona'),
        # ----- (8)  --------------------------------
        ('Natanael'*1000, 'natan'), 
        # +---+ 
        #   |
        #   +------>> String "suja" contendo um palíndromo:
        #             A repetição de Natanael 1000 vezes
        #             serve para dificultar a localização 
        #             do palíndromo `NATAN`; 
        #             E o fato dela ser muito grande é para
        #             forçar um << TimeOut >> .
         
    ]
    for i, (text, expected) in enumerate(CASES, start=1):
        text = normalize('NFKD', text).encode('ASCII', 'ignore').decode()
        text = re.sub(r'[ ,.?!:-;]', '', text.lower())
        print(f'Test case {i}:', end='')
        res = longest_palindromes(text)
        if res!= expected:
             print(f' expected {expected}, got {res}')
        assert res == expected
        print('...OK')
    print('SUCCESS!'.center(50, '*'))
    # =================================================================


if __name__ == '__main__':
     main()
