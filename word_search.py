"""
Resposta ao desafio em
https://leetcode.com/problems/word-search/
"""


class Solution:
    def exist(self, board: list, word: str) -> bool:
        # -------------------------------------------
        def back_track(x: int, y: int, k: int) -> bool:
            if len(word) == k:
                return True
            valid = all([
                0 <= y < len(board),
                0 <= x < len(board[0]),
            ])
            if not valid or board[y][x] != word[k]:
                return False
            board[y][x] = ' '
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                if back_track(x + dx, y + dy, k + 1):
                    return True
            board[y][x] = word[k]
            return False
        # -------------------------------------------
        for y in range(len(board)):
            for x in range(len(board[y])):
                if back_track(x, y, 0):
                    return True
        return False



if __name__ == '__main__':
    solution = Solution()
    CASES = [
        ('CEDILHA', True),
        ('APOIADO', False),
        ('AZUL', True),
        ('ARVORE', False),
        ('LARVA', True),
    ]
    for i, (text, expected) in enumerate(CASES, start=1):
        GRID = [
            #0   1   2   3   4   5
            ['D','C','E','E','E','M'], # 0
            ['E','L','A','D','I','A'], # 1
            ['C','E','R','V','O','D'], # 2
            ['K','D','I','A','P','T'], # 3
            ['A','H','L','Z','U','L'], # 4
        ]
        print(f'Teste {i} ({text})...')
        assert expected == solution.exist(GRID, text)
        print('\t...OK!')
    print('Passou em todos os testes'.center(50, '*'))
