"""
Resposta ao desafio em
https://leetcode.com/problems/word-search/
"""


class Solution:
    def __init__(self):
        self.map = {}

    def exist(self, board: list, word: str) -> bool:
        if not self.map:
            for y, row in enumerate(board):
                for x, char in enumerate(row):
                    self.map.setdefault(char, []).append((x, y))
        return self.matches(word)

    def matches(self, word: str) -> bool:
        self.path = None
        for i, char in enumerate(word):
            found = self.map.get(char, [])
            if not found:
                return False
            if self.path:
                self.update(found)
            elif i > 0:
                return False
            else:
                self.path = [[row] for row in found]
        return len(self.path) > 0

    def update(self, data: list) -> None:
        result = []
        while self.path:
            row = self.path.pop(0)
            x1, y1 = row[-1]
            for x2, y2 in data:
                closer = (abs(x2-x1), abs(y2-y1)) in [(0, 1), (1, 0)]
                unique = (x2, y2) not in row
                if closer and unique:
                    result.append( row + [(x2, y2)] )
        self.path = result



if __name__ == '__main__':
    GRID = [
        #012345
        'DCEEEM', # 0
        'ELADIA', # 1
        'CERVOD', # 2
        'KDIAPT', # 3
        'AHLZUL', # 4
    ]
    solution = Solution()
    CASES = [
        ('CEDILHA', True),
        ('APOIADO', False),
        ('AZUL', True),
        ('ARVORE', False),
    ]
    for i, (text, expected) in enumerate(CASES, start=1):
        print(f'Teste {i} ({text})...')
        res = solution.exist(GRID, text)
        assert res == expected
        print('\t...OK!')
    print('Passou em todos os testes'.center(50, '*'))
