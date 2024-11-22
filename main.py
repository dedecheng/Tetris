from tkinter.constants import HORIZONTAL

from src import *
import pygame
from pygame.locals import *

pygame.init()

# 設定視窗
GRID_SIZE = 30  # 方塊大小
WIDTH = 10
HEIGHT = 20
HORIZONTAL_BLANK = 6
WINDOW_WIDTH = (WIDTH + HORIZONTAL_BLANK * 2) * GRID_SIZE
WINDOW_HEIGHT = HEIGHT * GRID_SIZE
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()
bord_width = 2
max_touch_ground_times = 3
line_color = (50, 50, 50)  # 灰色


def game_loop():
    running = True
    game_manager = GameManager(WIDTH, HEIGHT)

    fall_time = 0
    fall_speed = 500  # 每 500 毫秒下墜一次
    current_touch_ground_times = 0
    enable_movement = True
    move_time = 0
    move_speed = 300
    while running:
        screen.fill((0, 0, 0))  # 將整個螢幕設置為黑色背景
        delta_time = clock.tick(30)
        fall_time += delta_time
        move_time += delta_time

        # 玩家輸入
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                enable_movement = False
                move_time = 0
                if event.key == K_LEFT:
                    game_manager.move_left()
                elif event.key == K_RIGHT:
                    game_manager.move_right()
                elif event.key == K_DOWN:
                    game_manager.move_down()
                elif event.key == K_UP:
                    game_manager.rotate_right()
                elif event.key == K_z:
                    game_manager.rotate_left()
                elif event.key == K_SPACE:
                    game_manager.straight_down()
                elif event.key == K_c:
                    game_manager.hold_block()
        # 偵測持續按鍵
        keys = pygame.key.get_pressed()
        if enable_movement:
            if keys[pygame.K_DOWN]:  # 按下「下」箭頭鍵
                game_manager.move_down()
            if keys[pygame.K_LEFT]:  # 按下「左」箭頭鍵
                game_manager.move_left()
            if keys[pygame.K_RIGHT]:  # 按下「右」箭頭鍵
                game_manager.move_right()

        # 自動下墜
        if fall_time > fall_speed:
            game_manager.move_down()
            if game_manager.ground_touched():
                current_touch_ground_times += 1
                if current_touch_ground_times >= max_touch_ground_times:
                    game_manager.place_block()
                    current_touch_ground_times = 0
            fall_time = 0

        if move_time > move_speed:
            enable_movement = True

        # 繪製棋盤
        for i in range(len(game_manager.board.board)):  # 遍歷列的索引
            for j in range(len(game_manager.board.board[i])):  # 遍歷元素的索引
                cell = game_manager.board.board[i][j]
                if cell:
                    color = Block.block_color[cell.value]
                    pygame.draw.rect(screen, color, (
                        (j + HORIZONTAL_BLANK) * GRID_SIZE, (HEIGHT - i - 1) * GRID_SIZE,
                        GRID_SIZE, GRID_SIZE))
                    # pygame.draw.rect(screen, color, (
                    #     j * GRID_SIZE + bord_width, (height - i - 1) * GRID_SIZE + bord_width,
                    #     GRID_SIZE - bord_width * 2, GRID_SIZE - bord_width * 2))

        # 繪製方塊
        for x, y in game_manager.current_block.cells:
            x += game_manager.current_block.pos[0]
            y += game_manager.current_block.pos[1]
            cell = game_manager.current_block.type
            if cell:
                color = Block.block_color[cell.value]
                pygame.draw.rect(screen, color,
                                 ((x + HORIZONTAL_BLANK) * GRID_SIZE, (HEIGHT - y - 1) * GRID_SIZE,
                                  GRID_SIZE, GRID_SIZE))
                # pygame.draw.rect(screen, color,
                #                  (x * GRID_SIZE + bord_width, (height - y - 1) * GRID_SIZE + bord_width,
                #                   GRID_SIZE - bord_width * 2, GRID_SIZE - bord_width * 2))

        # 繪製接下來的方塊
        for preview_num in range(game_manager.preview_count):
            for x, y in game_manager.blocks_queue[preview_num].cells:
                cell = game_manager.blocks_queue[preview_num].type
                if cell:
                    color = Block.block_color[cell.value]
                    pygame.draw.rect(screen, color,
                                     ((x + WIDTH + HORIZONTAL_BLANK + 2) * GRID_SIZE, ((preview_num + 1) * 3 - y) * GRID_SIZE,
                                      GRID_SIZE, GRID_SIZE))
        #繪製 hold 方塊
        if not game_manager.hold == None:
            hold_color = Block.block_color[game_manager.hold.type.value]
            for x, y in game_manager.hold.cells:
                cell = game_manager.hold.type
                pygame.draw.rect(screen, hold_color,
                                 ((x + 2) * GRID_SIZE, (2 - y) * GRID_SIZE,
                                  GRID_SIZE, GRID_SIZE))
        # 繪製棋盤格線
        for row in range(HEIGHT + 1):  # 繪製水平線
            pygame.draw.line(
                screen,
                line_color,
                (HORIZONTAL_BLANK * GRID_SIZE, row * GRID_SIZE),
                ((WIDTH + HORIZONTAL_BLANK) * GRID_SIZE, row * GRID_SIZE),
                1  # 線條寬度
            )
        for col in range(WIDTH + 1):  # 繪製垂直線
            pygame.draw.line(
                screen,
                line_color,
                ((col + HORIZONTAL_BLANK) * GRID_SIZE, 0),
                ((col + HORIZONTAL_BLANK) * GRID_SIZE, HEIGHT * GRID_SIZE),
                1  # 線條寬度
            )

        pygame.display.flip()

    pygame.quit()


game_loop()
