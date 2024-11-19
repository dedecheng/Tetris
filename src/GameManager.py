from src import *
import copy

class GameManager:
    def __init__(self, w, h):
        self.current_block = Block(BlockType.I, 0, 7, 10)  # 初始方塊
        self.board = Board()
        self.w = w
        self.h = h

    def rotate_left(self):
        old_direction = self.current_block.direction
        new_direction = Direction((self.current_block.direction.value + 3) % 4)

        # 計算旋轉後的新格子
        new_cells = [(-y, x) for x, y in self.current_block.cells]

        # wall kick
        if self.kick_wall(new_cells, old_direction, new_direction):
            # 成功更新方向
            self.current_block.direction = new_direction
        else:
            pass

    def rotate_right(self):
        old_direction = self.current_block.direction
        new_direction = Direction((self.current_block.direction.value + 1) % 4)

        # 計算旋轉後的新格子
        new_cells = [(y, -x) for x, y in self.current_block.cells]

        # wall kick
        if self.kick_wall(new_cells, old_direction, new_direction):
            # 成功更新方向
            self.current_block.direction = new_direction
        else:
            pass

    def kick_wall(self, new_cells, old_direction, new_direction):
        if self.current_block.type == BlockType.O:
            pass  # O 型不需要 wall kick
        elif self.current_block.type == BlockType.I:
            offsets = Block.WALL_KICKS_I.get((old_direction, new_direction), [(0, 0)])
        else:
            offsets = Block.WALL_KICKS.get((old_direction, new_direction), [(0, 0)])

        for offset_x, offset_y in offsets:
            origin_cells = self.current_block.cells
            # 計算應用偏移後的新格子
            self.current_block.cells = [(x + offset_x, y + offset_y) for x, y in new_cells]
            self.current_block.pos[0] += offset_x
            self.current_block.pos[1] += offset_y
            if not self.is_valid():
                self.current_block.cells = origin_cells
                self.current_block.pos[0] -= offset_x
                self.current_block.pos[1] -= offset_y
                return False

        return True  # 檢查所有偏移量後，若都無法有效旋轉，返回 False

    def is_valid(self):
        for x, y in self.current_block.cells:
            x += self.current_block.pos[0]
            y += self.current_block.pos[1]
            if x < 0 or x >= self.w or y < 0 or y >= self.h:  # 超出邊界
                return False
            if self.board.board[x][y] is not None:  # 與其他方塊重疊
                return False
        return True

    def move_right(self):
        self.current_block.pos[0] += 1
        if not self.is_valid():
            self.current_block.pos[0] -= 1

    def move_left(self):
        self.current_block.pos[0] -= 1
        if not self.is_valid():
            self.current_block.pos[0] += 1

    def move_down(self):
        self.current_block.pos[1] -= 1
        if not self.is_valid():
            self.current_block.pos[1] += 1

    def straight_down(self):
        self.current_block.pos[1] = 0
        if self.is_valid():
            self.current_block.pos[1] = 0

    def ground_touched(self):
        pass

    def place_block(self):
        self.board.place_block(self.current_block)
        # TODO
        # 放完之後，生成新方塊
