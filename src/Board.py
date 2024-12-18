class Board:
    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.board = [[None] * self.width for _ in range(self.height + 2)]

    def place_block(self, block):
        for cell in block.cells:
            self.board[block.pos[1] + cell[1]][block.pos[0] + cell[0]] = block.type

        return self.clear_full_lines()

    def clear_full_lines(self):
        line_cleared = 0
        i = 0
        while (i < self.height):
            line = self.board[i]
            full = True

            # check if line is full
            for cell in line:
                if cell == None:
                    full = False
                    break

            # line not full
            if not full:
                i += 1
                continue

            # clear line
            for j in range(len(line)):
                self.board[i][j] = None

            # move all line down
            for j in range(i + 1, self.height):
                for k in range(len(self.board[j])):
                    self.board[j - 1][k] = self.board[j][k]
            line_cleared += 1

        return line_cleared
