from enum import Enum

class BlockType(Enum):
    I = 1
    J = 2
    L = 3
    O = 4
    S = 5
    Z = 6
    T = 7

class Direction(Enum):
    initial = 0
    R = 1
    upside_down = 2
    L = 3


class Block():
    def __init__(self):
        self.pos = [0, 0]  # 重心x,y座標
        self.type = BlockType.I  # BlockType
        self.direction = Direction.initial  # 方向
        self.touch_ground = 0 #接觸地板時間

    def rotate_left(self, board, w, h):
        pass

    def rotate_right(self, board, w, h):
        pass

    def is_valid(self, board, w, h):
        pass

    def move_right(self, board, w, h):
        pass

    def move_left(self, board, w, h):
        pass

    def move_down(self, board, w, h):
        pass

    def straight_down(self, board, w, h):
        pass

    def ground_touched(self, board, w, h):
        pass