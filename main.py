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

def game_loop():
    running = True
    game_manager = GameManager(width, height)

    fall_time = 0
    fall_speed = 500  # 每 500 毫秒下墜一次

    while running:
        screen.fill((0, 0, 0))  # 將整個螢幕設置為黑色背景
        delta_time = clock.tick(60)
        fall_time += delta_time

        # 玩家輸入
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
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

        # 自動下墜
        if fall_time > fall_speed:
            game_manager.move_down()
            if game_manager.ground_touched:
                game_manager.place_block()
            fall_time = 0

        # 繪製棋盤
        for i in range(len(game_manager.board.board)):  # 遍歷列的索引
            for j in range(len(game_manager.board.board[i])):  # 遍歷元素的索引
                cell = game_manager.board.board[i][j]
                if cell:
                    pygame.draw.rect(screen, cell, ((width-i) * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        for y, row in enumerate(game_manager.board.grid):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, cell, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        # 繪製方塊
        for y, row in enumerate(current_block.shape):
            for x, cell in enumerate(row):
                if cell:
                    grid_x = current_block.position[0] + x
                    grid_y = current_block.position[1] + y
                    pygame.draw.rect(screen, current_block.color,
                                     (grid_x * GRID_SIZE, grid_y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        pygame.display.flip()

    pygame.quit()


game_loop()
