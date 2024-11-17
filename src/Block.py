from enum import Enum

import Board

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
    
    def __init__(self, block_type, direction):
        self.cells = self.initial_cell(block_type)  # 相對於重心的位置
        self.pos = [0, 0]  # 重心的 (x, y) 座標
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
    
    def rotate_left(self, w, h):
        old_direction = self.direction
        new_direction = Direction((self.direction.value - 1) % 4)
    
        # 計算旋轉後的新格子
        new_cells = [(-y, x) for x, y in self.cells]
    
        # wall kick
        if self.kick_wall(self, w, h, new_cells, old_direction, new_direction):
        # 成功更新方向
            self.direction = new_direction
        else:
            pass
                        
    def rotate_right(self, w, h):
        old_direction = self.direction
        new_direction = Direction((self.direction.value + 1) % 4)
    
        # 計算旋轉後的新格子
        new_cells = [(y, -x) for x, y in self.cells]
    
        # wall kick
        if self.kick_wall(self, w, h, new_cells, old_direction, new_direction):
        # 成功更新方向
            self.direction = new_direction
        else:
            pass
       
    def kick_wall(self, w, h, new_cells, old_direction, new_direction):
        if self.type == BlockType.O:
            pass  # O 型不需要 wall kick
        elif self.type == BlockType.I:
            offsets = self.WALL_KICKS_I.get((old_direction, new_direction), [(0, 0)])
        else:
            offsets = self.WALL_KICKS.get((old_direction, new_direction), [(0, 0)])
        
        for offset_x, offset_y in offsets:
            # 計算應用偏移後的新格子
            adjusted_cells = [(x + offset_x, y + offset_y) for x, y in new_cells]
            if self.is_valid(w, h, adjusted_cells):
                self.cells = adjusted_cells
                self.pos[0] += offset_x
                self.pos[1] += offset_y
                return True

        return False  # 檢查所有偏移量後，若都無法有效旋轉，返回 False

         
    def is_valid(self, w, h, cells):
     for x, y in cells:
         if x < 0 or x >= w or y < 0 or y >= h:  # 超出邊界
             return False
         if Board[y][x] != 0:  # 與其他方塊重疊
             return False
     return True

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