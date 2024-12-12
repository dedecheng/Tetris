from copy import deepcopy

from pygame.draw import lines

from src import *
import random
import queue
from collections import deque
from enum import Enum
import json
import os

class GameState(Enum):
    Playing = 0
    GameOver = 1
    Paused = 2

class GameManager:
    def __init__(self, w, h):
        self.board = Board(w, h)
        self.w = w
        self.h = h
        self.preview_count = 3
        self.blocks_queue = deque()
        self.hold = None
        self.is_hold = False
        self.generate_pos = [int(w / 2), int(h)]
        self.current_block = self.next_block()  # 初始方塊
        self.preview_block = self.current_block
        self.line_cleared = 0
        self.score = 0
        self.game_state = GameState.Playing
        self.player_name = "ray"
        self.game_level = 1
        self.last_move_rotate = False

    def update_preview_block(self):
        self.preview_block = deepcopy(self.current_block)
        for _ in range(self.board.height):
            self.preview_block.pos[1] -= 1
            if not is_valid(self.preview_block, self.board):
                self.preview_block.pos[1] += 1

    def rotate_left(self):
        old_direction = self.current_block.direction
        new_direction = Direction((self.current_block.direction.value + 3) % 4)

        # 計算旋轉後的新格子
        new_cells = [(-y, x) for x, y in self.current_block.cells]

        # wall kick
        if self.kick_wall(new_cells, old_direction, new_direction):
            # 成功更新方向
            self.current_block.direction = new_direction
            self.last_move_rotate = True
        else:
            pass

        self.update_preview_block()

    def hold_block(self):
        if self.is_hold:
            return
        if self.hold == None :
            self.hold = Block(self.current_block.type, Direction.initial, self.generate_pos[0], self.generate_pos[1])
            self.current_block = self.next_block()
        else:
            new_block = self.hold
            self.hold = Block(self.current_block.type, Direction.initial, self.generate_pos[0], self.generate_pos[1])
            self.current_block = new_block
        self.is_hold = True
        self.update_preview_block()

    def rotate_right(self):
        old_direction = self.current_block.direction
        new_direction = Direction((self.current_block.direction.value + 1) % 4)

        # 計算旋轉後的新格子
        new_cells = [(y, -x) for x, y in self.current_block.cells]

        # wall kick
        if self.kick_wall(new_cells, old_direction, new_direction):
            # 成功更新方向
            self.current_block.direction = new_direction
            self.last_move_rotate = True

        else:
            pass
        self.update_preview_block()


    def kick_wall(self, new_cells, old_direction, new_direction):
        if self.current_block.type == BlockType.O:
            return False # O 型不需要 wall kick
        elif self.current_block.type == BlockType.I:
            offsets = Block.WALL_KICKS_I.get((old_direction, new_direction), [(0, 0)])
        else:
            offsets = Block.WALL_KICKS.get((old_direction, new_direction), [(0, 0)])

        origin_cells = self.current_block.cells[:]
        self.current_block.cells = [(x, y) for x, y in new_cells]
        for offset_x, offset_y in offsets:
            # 計算應用偏移後的新格子
            self.current_block.pos[0] += offset_x
            self.current_block.pos[1] += offset_y
            if is_valid(self.current_block, self.board):
                return True
            self.current_block.pos[0] -= offset_x
            self.current_block.pos[1] -= offset_y
        self.current_block.cells = origin_cells
        return False  # 檢查所有偏移量後，若都無法有效旋轉，返回 False

    # def is_valid(self):
    #     for x, y in self.current_block.cells:
    #         x += self.current_block.pos[0]
    #         y += self.current_block.pos[1]
    #         if x < 0 or x >= self.w or y < 0 or y >= self.h:  # 超出邊界
    #             return False
    #         if self.board.board[y][x] is not None:  # 與其他方塊重疊
    #             return False
    #     return True

    def move_right(self):
        self.current_block.pos[0] += 1
        if not is_valid(self.current_block, self.board):
            self.current_block.pos[0] -= 1
        else:
            self.last_move_rotate = False

        self.update_preview_block()


    def move_left(self):
        self.current_block.pos[0] -= 1
        if not is_valid(self.current_block, self.board):
            self.current_block.pos[0] += 1
        else:
            self.last_move_rotate = False
        self.update_preview_block()


    def move_down(self):
        self.current_block.pos[1] -= 1
        if not is_valid(self.current_block, self.board):
            self.current_block.pos[1] += 1
        else:
            self.last_move_rotate = False
        self.update_preview_block()


    def straight_down(self):
        for _ in range(self.board.height):
            self.move_down()
        self.place_block()

    def ground_touched(self):
        self.current_block.pos[1] -= 1
        if not is_valid(self.current_block, self.board):
            self.current_block.pos[1] += 1
            return True
        self.current_block.pos[1] += 1
        return False

    def place_block(self):
        line_cleared = self.board.place_block(self.current_block)
        self.score_update(line_cleared)
        self.line_cleared += line_cleared

        # 更新遊戲狀態
        if self.check_gameover():
             return
        # TODO
        # 放完之後，生成新方塊
        self.current_block = self.next_block()

        self.update_preview_block()


        # 更新is_hold
        self.is_hold = False


    def next_block(self):
        # 方塊類型列表（俄羅斯方塊的 7 種形狀）
        block_types = list(BlockType)
        """補充預覽方塊到隊列中"""
        while len(self.blocks_queue) <= self.preview_count:
            # 生成新的方塊袋並打亂順序
            new_bag = random.sample(block_types, len(block_types))
            self.blocks_queue.extend(
                Block(type, Direction.initial, self.generate_pos[0], self.generate_pos[1]) for type in new_bag)

        """取出下一個方塊"""
        # 取出下一個方塊
        return self.blocks_queue.popleft()

    def check_gameover(self):
        # check if game is over
        for cell in self.board.board[self.board.height]:
            if not cell == None:
                self.game_state = GameState.GameOver
                self.record_score()
                return True

        return False

    def score_update(self, lines):
        block_corner = 0
        if self.current_block.type == BlockType.T and self.last_move_rotate:
            x, y = self.current_block.pos
            if x == 0:
                if y == 0 or y == self.h - 1:
                    block_corner = 0
                else:
                    block_corner += 2
                    if self.board.board[y - 1][x + 1] == None:
                        block_corner += 1
                    if self.board.board[y + 1][x + 1] == None:
                        block_corner += 1
            elif x == self.w - 1:
                if y == 0 or y == self.h - 1:
                    block_corner = 0
                else:
                    block_corner += 2
                    if self.board.board[y - 1][x - 1] == None:
                        block_corner += 1
                    if self.board.board[y + 1][x - 1] == None:
                        block_corner += 1
            elif y == 0:
                block_corner += 2
                if self.board.board[y + 1][x - 1] == None:
                    block_corner += 1
                if self.board.board[y + 1][x + 1] == None:
                    block_corner += 1
            elif y == self.h - 1:
                block_corner += 2
                if self.board.board[y - 1][x - 1] == None:
                    block_corner += 1
                if self.board.board[y - 1][x + 1] == None:
                    block_corner += 1
            else :
                if self.board.board[y + 1][x - 1] == None:
                    block_corner += 1
                if self.board.board[y + 1][x + 1] == None:
                    block_corner += 1
                if self.board.board[y - 1][x - 1] == None:
                    block_corner += 1
                if self.board.board[y - 1][x + 1] == None:
                    block_corner += 1

        if block_corner >= 3:
            if lines == 0:
                self.score += 100
            elif lines == 1:
                self.score += 500
            elif lines == 2:
                self.score += 800
            elif lines == 3:
                self.score += 1200
        else:
            if lines == 0:
                return
            elif lines == 1:
                self.score += 100
            elif lines == 2:
                self.score += 300
            elif lines == 3:
                self.score += 500
            elif lines == 4:
                self.score += 800
    def record_score(self):

        file_path = "./assets/ranking_board.json"
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            rank = len(data)
            while rank > 0:
                if data[rank - 1]['score'] < self.score:
                    if not rank == 10:
                        if len(data) <= rank:
                            data.append(data[rank - 1])
                        else:
                            data[rank] = data[rank - 1]
                    rank -= 1
                else:
                    break
            #比前十名更高分
            if not rank == 10:
                new_score = {"name": self.player_name, "line": self.line_cleared, "score": self.score}
                if len(data) <= rank:
                    data.append(new_score)
                else:
                    data[rank] = new_score

                with open(file_path, "w", encoding="utf-8") as file:
                    json.dump(data, file, ensure_ascii=False, indent=4)

        else:
            data = []
            first_score = {"name" : self.player_name, "line" : self.line_cleared, "score" : self.score}
            data.append(first_score)
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)




def is_valid(block, board):
    for x, y in block.cells:
        x += block.pos[0]
        y += block.pos[1]
        if x < 0 or x >= board.width or y < 0 or y >= board.height + 2:  # 超出邊界(加上頂端方塊生成空間)
            return False
        if board.board[y][x] is not None:  # 與其他方塊重疊
            return False
    return True