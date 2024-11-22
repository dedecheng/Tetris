from src.Block import BlockType, Block


class Board:
    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.board = [[None] * self.width for _ in range(self.height)]



    def place_block(self, block):
        for cell in block.cells:
            self.board[block.pos[1] + cell[1]][block.pos[0] + cell[0]] = block.type

        self.clear_full_lines()

    def clear_full_lines(self):
        i = 0
        while(i < self.height):
            line = self.board[i]
            full = True
            for cell in line:
                if cell == None:
                    full = False
                    break

            if not full:
                i += 1
                continue

            for j in range(len(line)):
                self.board[i][j] = None

            for j in range(i + 1, self.height):
                for k in range(len(self.board[j])):
                    self.board[j - 1][k] = self.board[j][k]


