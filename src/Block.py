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
        self.centroid = [0, 0]  # 重心x,y座標
        self.type = BlockType.I  # BlockType
        self.direction = Direction.initial  # 方向
