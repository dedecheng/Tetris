from tkinter.constants import HORIZONTAL, VERTICAL
from turtle import Screen

from src import *
import pygame
from pygame.locals import *

from src.GameManager import GameState
import src.global_var as global_var
import math
from pathlib import Path

pygame.init()

# 設定視窗
GRID_SIZE = 30  # 方塊大小
WIDTH = global_var.WIDTH
HEIGHT = 20
HORIZONTAL_BLANK = 2
VERTICAL_BLANK = 1
BOTTON_MARGIN = 1.5
WINDOW_WIDTH = (WIDTH + HORIZONTAL_BLANK * 2 + 10) * GRID_SIZE
WINDOW_HEIGHT = (HEIGHT + VERTICAL_BLANK + BOTTON_MARGIN) * GRID_SIZE
PREVIEW_OFFSET = WIDTH + 19
PREVIEW_WIDTH = 5  # 預覽區域的寬度（以格子為單位）
PREVIEW_HEIGHT = 13  # 預覽區域的高度（以格子為單位）
PREVIEW_GRID_SIZE = GRID_SIZE // 2  # 預覽區域內方塊縮小一半
INIT_FALL_SPEED = 500  # 每 500 毫秒下墜一次
LINES_TO_SPEEDUP = 5

root_dir = Path(__file__).parent.parent
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()
bord_width = 2
max_touch_ground_number = 10
line_color = (255, 255, 255)  # 灰色
transparency = 75
background_image = pygame.image.load(str(root_dir) + r'.\assets\pictures\Group 6.png')
background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))


def draw_pause_button():
    """繪製暫停按鈕"""
    PAUSE_BUTTON_RECT = pygame.Rect(WINDOW_WIDTH - 50, 10, 30, 30)  # 暫停按鈕的區域
    pygame.draw.rect(screen, (255, 255, 255), PAUSE_BUTTON_RECT, border_radius=5)  # 白色按鈕背景
    pygame.draw.rect(screen, (171, 209, 198), (WINDOW_WIDTH - 43, 15, 8, 20))  # 左豎線
    pygame.draw.rect(screen, (171, 209, 198), (WINDOW_WIDTH - 28, 15, 8, 20))  # 右豎線
    return PAUSE_BUTTON_RECT


def initialize():
    global WIDTH
    global WINDOW_WIDTH
    global PREVIEW_OFFSET
    global screen
    global clock
    global background_image
    global INIT_FALL_SPEED
    WIDTH = global_var.WIDTH
    WINDOW_WIDTH = (WIDTH + HORIZONTAL_BLANK * 2 + 10) * GRID_SIZE
    PREVIEW_OFFSET = WIDTH + 19

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    background_image = pygame.image.load(str(root_dir) + r'.\assets\pictures\Group 6.png')
    background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))


    INIT_FALL_SPEED = max(1000 - global_var.SPEED * 100, 10)


def game_loop():
    initialize()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    running = True
    game_manager = GameManager(WIDTH, HEIGHT)
    game_manager.player_name = global_var.PLAYER_NAME
    fall_time = 0
    fall_speed = INIT_FALL_SPEED
    current_touch_ground_number = 0
    enable_movement = True
    move_time = 0
    move_speed = 150
    elapsed_time = 0
    touch_ground_time = 0
    touch_ground_speed = 1000
    while running:
        screen.fill((171, 209, 198))  # screem color

        screen.blit(background_image, (60, -30))

        pygame.draw.rect(
            screen,
            (255, 255, 255),  # 邊框顏色：白色
            (
                HORIZONTAL_BLANK * GRID_SIZE - 12,  # 左上角 X（稍微往左移）
                VERTICAL_BLANK * GRID_SIZE - 12,  # 左上角 Y（稍微往上移）
                WIDTH * GRID_SIZE + 25,  # 寬度（稍微增寬）
                HEIGHT * GRID_SIZE + 25  # 高度（稍微增高）
            ),
            40,  # 邊框厚度
            border_radius=5
        )

        pygame.draw.rect(
            screen,
            (249, 188, 96),  # board color
            (
                HORIZONTAL_BLANK * GRID_SIZE,  # 棋盤左上角 X 坐標
                VERTICAL_BLANK * GRID_SIZE,  # 棋盤左上角 Y 坐標
                WIDTH * GRID_SIZE,  # 棋盤寬度
                HEIGHT * GRID_SIZE  # 棋盤高度
            )
        )

        PAUSE_BUTTON_RECT = draw_pause_button()

        delta_time = clock.tick(30)
        if game_manager.game_state == GameState.Playing:
            fall_time += delta_time
            move_time += delta_time
            elapsed_time += delta_time

        # speed up and update game_level
        game_manager.game_level = min(elapsed_time // 30000 + 1, 10)
        fall_speed = max(int(INIT_FALL_SPEED - 50 * game_manager.game_level), 10)

        # 玩家輸入
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                return
            if event.type == MOUSEBUTTONDOWN:
                if PAUSE_BUTTON_RECT.collidepoint(event.pos):  # 檢測是否點擊暫停按鈕
                    # 切換暫停狀態
                    if game_manager.game_state == GameState.Paused:
                        game_manager.game_state = GameState.Playing
                    else:
                        game_manager.game_state = GameState.Paused
            if game_manager.game_state == GameState.Playing and event.type == KEYDOWN:  # 只有在未暫停時處理按鍵事件
                enable_movement = False
                move_time = 0
                if event.key == K_LEFT:
                    game_manager.move_left()
                elif event.key == K_RIGHT:
                    game_manager.move_right()
                elif event.key == K_DOWN:
                    game_manager.move_down()
                    fall_time = 0
                elif event.key == K_UP:
                    game_manager.rotate_right()
                    if game_manager.ground_touched():
                        current_touch_ground_number += 1
                        if current_touch_ground_number < max_touch_ground_number:
                            touch_ground_time = 0
                elif event.key == K_z:
                    game_manager.rotate_left()
                    if game_manager.ground_touched():
                        current_touch_ground_number += 1
                        if current_touch_ground_number < max_touch_ground_number:
                            print(current_touch_ground_number)
                            touch_ground_time = 0
                elif event.key == K_SPACE:
                    game_manager.straight_down()
                elif event.key == K_c:
                    game_manager.hold_block()

        if game_manager.game_state == GameState.Playing:
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
                fall_time = 0

            # 偵測延遲鎖定
            if game_manager.ground_touched():
                touch_ground_time += delta_time
                if touch_ground_time >= touch_ground_speed:
                    game_manager.place_block()
                    touch_ground_time = 0
                    current_touch_ground_number = 0

            if move_time > move_speed:
                enable_movement = True

        if game_manager.game_state == GameState.Paused:  # 如果暫停，顯示「暫停」提示
            font = pygame.font.SysFont('Arial', 50)
            pause_text = font.render('Paused', True, (255, 255, 255))
            pause_rect = pause_text.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
            screen.blit(pause_text, pause_rect)

        # 繪製棋盤
        for i in range(len(game_manager.board.board)):  # 遍歷棋盤
            for j in range(len(game_manager.board.board[i])):
                cell = game_manager.board.board[i][j]
                if cell:
                    color = Block.block_color[cell.value]
                    pygame.draw.rect(
                        screen,
                        color,
                        (
                            (j + HORIZONTAL_BLANK) * GRID_SIZE,  # X 坐標
                            (HEIGHT - i - 1 + VERTICAL_BLANK) * GRID_SIZE,  # Y 坐標
                            GRID_SIZE,  # 矩形寬度
                            GRID_SIZE  # 矩形高度
                        ),
                        border_radius=5  # 圓角半徑
                    )
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
                pygame.draw.rect(
                    screen,
                    color,
                    (
                        (x + HORIZONTAL_BLANK) * GRID_SIZE,
                        (HEIGHT - y - 1 + VERTICAL_BLANK) * GRID_SIZE,
                        GRID_SIZE,
                        GRID_SIZE
                    ),
                    border_radius=5
                )

        # 繪製落下位置
        transparency_surface = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
        for x, y in game_manager.preview_block.cells:
            x += game_manager.preview_block.pos[0]
            y += game_manager.preview_block.pos[1]
            cell = game_manager.preview_block.type
            if cell:
                color = Block.block_color[cell.value]
                transparency_surface.fill((color[0], color[1], color[2], transparency))
                screen.blit(transparency_surface,
                            ((x + HORIZONTAL_BLANK) * GRID_SIZE, (HEIGHT - y - 1 + VERTICAL_BLANK) * GRID_SIZE))

        pygame.draw.rect(
            screen,
            (255, 255, 255),  # 白色邊框顏色
            (
                16 * 25 - 5,  # 邊框左上角 X（稍微向左偏移）
                VERTICAL_BLANK * GRID_SIZE - 5,  # 邊框左上角 Y（稍微向上偏移）
                PREVIEW_WIDTH * PREVIEW_GRID_SIZE + 10,  # 寬度（稍微增寬）
                PREVIEW_HEIGHT * PREVIEW_GRID_SIZE + 10  # 高度（稍微增高）
            ),
            5,  # 邊框厚度
            border_radius=5
        )

        pygame.draw.rect(
            screen,
            (249, 188, 96),  # 黑色背景
            (
                16 * 25,  # 預覽框左上角 X
                VERTICAL_BLANK * GRID_SIZE,  # 預覽框左上角 Y
                PREVIEW_WIDTH * PREVIEW_GRID_SIZE,  # 預覽框寬度
                PREVIEW_HEIGHT * PREVIEW_GRID_SIZE  # 預覽框高度
            )
        )

        # 繪製接下來的方塊
        for preview_num in range(game_manager.preview_count):
            for x, y in game_manager.blocks_queue[preview_num].cells:
                cell = game_manager.blocks_queue[preview_num].type
                if cell:
                    color = Block.block_color[cell.value]
                    pygame.draw.rect(
                        screen,
                        color,
                        (
                            (x + PREVIEW_OFFSET) * PREVIEW_GRID_SIZE,
                            ((preview_num + 1) * 3 - y + VERTICAL_BLANK) * PREVIEW_GRID_SIZE,
                            PREVIEW_GRID_SIZE,
                            PREVIEW_GRID_SIZE
                        ),
                        border_radius=2  # 減小圓角半徑，因為預覽區塊較小
                    )

        # 繪製 hold 方塊
        if not game_manager.hold == None:
            hold_color = Block.block_color[game_manager.hold.type.value]
            for x, y in game_manager.hold.cells:
                pygame.draw.rect(
                    screen,
                    hold_color,
                    (
                        (x + 2) * GRID_SIZE,  # X 坐標
                        (2 - y + VERTICAL_BLANK) * GRID_SIZE,  # Y 坐標
                        GRID_SIZE,
                        GRID_SIZE
                    ),
                    border_radius=5
                )

        # 繪製棋盤格線
        for row in range(HEIGHT + 1):  # 繪製水平線
            pygame.draw.line(
                screen,
                line_color,
                (HORIZONTAL_BLANK * GRID_SIZE, (row + VERTICAL_BLANK) * GRID_SIZE),
                ((WIDTH + HORIZONTAL_BLANK) * GRID_SIZE, (row + VERTICAL_BLANK) * GRID_SIZE),
                1  # 線條寬度
            )
        for col in range(WIDTH + 1):  # 繪製垂直線
            pygame.draw.line(
                screen,
                line_color,
                ((col + HORIZONTAL_BLANK) * GRID_SIZE, VERTICAL_BLANK * GRID_SIZE),
                ((col + HORIZONTAL_BLANK) * GRID_SIZE, (HEIGHT + VERTICAL_BLANK) * GRID_SIZE),
                1  # 線條寬度
            )
        if game_manager.game_state == GameState.GameOver:
            font = pygame.font.SysFont('Arial', 50)
            text_surface = font.render('Game Over', True, (255, 255, 255), (0, 0, 0))
            text_rect = text_surface.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
            screen.blit(text_surface, text_rect)

        # 顯示消除行數
        font = pygame.font.SysFont('Arial', 20)
        text_surface = font.render('line clear: ' + str(game_manager.line_cleared), True, (255, 255, 255))
        screen.blit(text_surface, (WINDOW_WIDTH - 120, 0))

        # 顯示分數
        font = pygame.font.SysFont('Arial', 20)
        text_surface = font.render('score: ' + str(game_manager.score), True, (255, 255, 255))
        screen.blit(text_surface, (WINDOW_WIDTH - 120, 30))

        # 顯示時間
        font = pygame.font.SysFont('Arial', 20)
        text_surface = font.render('time: ' + f"{elapsed_time / 1000} seconds", True, (255, 255, 255))
        screen.blit(text_surface, (WINDOW_WIDTH - 120, 60))

        # 顯示level
        font = pygame.font.SysFont('Arial', 20)
        text_surface = font.render('level: ' + f"{game_manager.game_level}", True, (255, 255, 255))
        screen.blit(text_surface, (WINDOW_WIDTH - 120, 90))
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    game_loop()
