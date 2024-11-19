from enum import Enum
import copy
import Board

block_color = [
    (0, 255, 255),
    (0, 0, 255),
    (255, 165, 0),
    (255, 255, 0),
    (0, 255, 0),
    (255, 0, 255),
    (255, 0, 0)
]

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


class Block:
    WALL_KICKS = {
        (Direction.initial, Direction.R): [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],
        (Direction.R, Direction.initial): [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],
        (Direction.R, Direction.upside_down): [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],
        (Direction.upside_down, Direction.R): [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],
        (Direction.upside_down, Direction.L): [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)],
        (Direction.L, Direction.upside_down): [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],
        (Direction.L, Direction.initial): [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],
        (Direction.initial, Direction.L): [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)],
    }

    WALL_KICKS_I = {
        (Direction.initial, Direction.R): [(0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2)],
        (Direction.R, Direction.initial): [(0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)],
        (Direction.R, Direction.upside_down): [(0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1)],
        (Direction.upside_down, Direction.R): [(0, 0), (1, 0), (-2, 0), (1, -2), (-2, 1)],
        (Direction.upside_down, Direction.L): [(0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)],
        (Direction.L, Direction.upside_down): [(0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2)],
        (Direction.L, Direction.initial): [(0, 0), (1, 0), (-2, 0), (1, -2), (-2, 1)],
        (Direction.initial, Direction.L): [(0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1)],
    }

    def __init__(self, block_type, direction, x, y):
        self.cells = self.initial_cell(block_type)  # 相對於重心的位置
        self.pos = [x, y]  # 重心的 (x, y) 座標
        self.type = block_type  # BlockType
        self.direction = direction  # 方向
        self.touch_ground = 0  # 接觸地板時間

    def initial_cell(self, block_type):
        if block_type == BlockType.I:
            return [(-2, 0), (-1, 0), (0, 0), (1, 0)]  # I 型
        elif block_type == BlockType.J:
            return [(-1, 1), (-1, 0), (0, 0), (1, 0)]  # J 型
        elif block_type == BlockType.L:
            return [(-1, 0), (0, 0), (1, 0), (1, 1)]  # L 型
        elif block_type == BlockType.O:
            return [(0, 0), (0, 1), (1, 0), (1, 1)]  # O 型
        elif block_type == BlockType.S:
            return [(-1, 0), (0, 0), (0, 1), (1, 1)]  # S 型
        elif block_type == BlockType.Z:
            return [(-1, 1), (0, 1), (0, 0), (1, 0)]  # Z 型
        elif block_type == BlockType.T:
            return [(-1, 1), (0, 1), (0, 0), (1, 0)]  # T 型
        else:
            return []  # 默認情況返回空


