from src.Block import BlockType, Block


class Board:
    def __init__(self):
        self.width = 10
        self.height = 20
        self.board = [[None] * self.width for _ in range(self.height)]
        self.active_block = Block()
        self.hold = BlockType.I

    def place_block(self, block):
        for cell in block.cells:
            self.board[cell[1]][cell[0]] = block.type

        self.clear_full_lines()

    def clear_full_lines(self):
        for i in range(self.height):
            line = self.board[i]
            full = True
            for cell in line:
                if cell == None:
                    full = False
                    break

            if not full:
                break

            for cell in line:
                cell = None

            for j in range(i + 1, self.height):
                current_line = self.board[j]
                past_line = self.board[j - 1]

                past_line = current_line

            i -= 1

