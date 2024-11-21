from src import *
import pygame
from pygame.locals import *

pygame.init()

# 設定視窗
WINDOW_WIDTH = 300
WINDOW_HEIGHT = 600
GRID_SIZE = 30  # 方塊大小
width = 10
height = 20
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()
bord_width = 2
max_touch_ground_times = 3
line_color = (50, 50, 50)  # 灰色


def game_loop():
    running = True
    game_manager = GameManager(width, height)

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
                        j * GRID_SIZE, (height - i - 1) * GRID_SIZE,
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
                                 (x * GRID_SIZE, (height - y - 1) * GRID_SIZE,
                                  GRID_SIZE, GRID_SIZE))
                # pygame.draw.rect(screen, color,
                #                  (x * GRID_SIZE + bord_width, (height - y - 1) * GRID_SIZE + bord_width,
                #                   GRID_SIZE - bord_width * 2, GRID_SIZE - bord_width * 2))

        # 繪製棋盤格線
        for row in range(height + 1):  # 繪製水平線
            pygame.draw.line(
                screen,
                line_color,
                (0, row * GRID_SIZE),
                (width * GRID_SIZE, row * GRID_SIZE),
                1  # 線條寬度
            )
        for col in range(width + 1):  # 繪製垂直線
            pygame.draw.line(
                screen,
                line_color,
                (col * GRID_SIZE, 0),
                (col * GRID_SIZE, height * GRID_SIZE),
                1  # 線條寬度
            )

        pygame.display.flip()

    pygame.quit()


game_loop()
