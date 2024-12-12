import pygame
import sys
from src.Button import Button, get_font
import src.global_var as global_var
# 初始化 Pygame
pygame.init()

# 窗口設定
SCREENWIDTH = 720
SCREENHEIGHT = 540
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption("設定")
font_size = 50
font = get_font(font_size)
MAX_VOLUME = 2
MIN_VOLUME = 0
MAX_SPEED = 10
MIN_SPEED = 1
MAX_WIDTH = 10
MIN_WIDTH = 4
def setting_page():
    # 初始化參數
    volume = 1

    running = True
    while running:
        screen.fill((107, 174, 185))  # 深藍色背景
        pygame.draw.rect(screen, (249, 188, 96),
                         (SCREENWIDTH / 20, SCREENHEIGHT / 18, 18 * SCREENWIDTH / 20, 16 * SCREENHEIGHT / 18))
        #sound
        sound_surface = font.render("Sound", True, (0, 70, 67))
        screen.blit(sound_surface, (3 * SCREENWIDTH / 20, 3 * SCREENHEIGHT / 20))
        sound_plus_button = Button(17 * SCREENWIDTH / 20, 3 * SCREENHEIGHT / 20, SCREENWIDTH / 20, SCREENWIDTH / 20,
                                   "+", font, (43, 97, 105), (225, 97, 98), (0, 70, 67))
        sound_minus_button = Button(7 * SCREENWIDTH / 20, 3 * SCREENHEIGHT / 20, SCREENWIDTH / 20, SCREENWIDTH / 20,
                                    "-", font, (43, 97, 105), (225, 97, 98), (0, 70, 67))

        sound_plus_button.draw(screen)
        sound_minus_button.draw(screen)
        rect = pygame.Rect(17 * SCREENWIDTH / 40, 3 * SCREENHEIGHT / 20 + SCREENWIDTH / 80, 16 * SCREENWIDTH / 40,
                           SCREENWIDTH / 40)
        pygame.draw.rect(screen, (43, 97, 105), rect, border_radius=100)
        rect = pygame.Rect(17 * SCREENWIDTH / 40, 3 * SCREENHEIGHT / 20 + SCREENWIDTH / 80,
                           16 * SCREENWIDTH / 40 * ((volume - MIN_VOLUME) / (MAX_VOLUME - MIN_VOLUME)), SCREENWIDTH / 40)
        pygame.draw.rect(screen, (225, 97, 98), rect, border_radius=100)

        #speed
        speed_surface = font.render("Speed", True, (0, 70, 67))
        screen.blit(speed_surface, (3 * SCREENWIDTH / 20, 6 * SCREENHEIGHT / 20))
        speed_plus_button = Button(17 * SCREENWIDTH / 20, 6 * SCREENHEIGHT / 20, SCREENWIDTH / 20, SCREENWIDTH / 20,
                                   "+", font, (43, 97, 105), (225, 97, 98), (0, 70, 67))
        speed_minus_button = Button(7 * SCREENWIDTH / 20, 6 * SCREENHEIGHT / 20, SCREENWIDTH / 20, SCREENWIDTH / 20,
                                    "-", font, (43, 97, 105), (225, 97, 98), (0, 70, 67))

        speed_plus_button.draw(screen)
        speed_minus_button.draw(screen)
        rect = pygame.Rect(17 * SCREENWIDTH / 40, 6 * SCREENHEIGHT / 20 + SCREENWIDTH / 80, 16 * SCREENWIDTH / 40,
                           SCREENWIDTH / 40)
        pygame.draw.rect(screen, (43, 97, 105), rect, border_radius=100)
        rect = pygame.Rect(17 * SCREENWIDTH / 40, 6 * SCREENHEIGHT / 20 + SCREENWIDTH / 80,
                           16 * SCREENWIDTH / 40 * ((global_var.SPEED - MIN_SPEED) / (MAX_SPEED - MIN_SPEED)),
                           SCREENWIDTH / 40)
        pygame.draw.rect(screen, (225, 97, 98), rect, border_radius=100)

        #width
        width_surface = font.render("Width", True, (0, 70, 67))
        screen.blit(width_surface, (3 * SCREENWIDTH / 20, 9 * SCREENHEIGHT / 20))
        width_plus_button = Button(11 * SCREENWIDTH / 20, 9 * SCREENHEIGHT / 20, SCREENWIDTH / 20, SCREENWIDTH / 20,
                                   "+", font, (43, 97, 105), (225, 97, 98), (0, 70, 67))
        width_minus_button = Button(7 * SCREENWIDTH / 20, 9 * SCREENHEIGHT / 20, SCREENWIDTH / 20, SCREENWIDTH / 20,
                                    "-", font, (43, 97, 105), (225, 97, 98), (0, 70, 67))
        width_plus_button.draw(screen)
        width_minus_button.draw(screen)

        rect = pygame.Rect(35 * SCREENWIDTH / 80, 9 * SCREENHEIGHT / 20, 3 * SCREENWIDTH / 40,
                           SCREENWIDTH / 20)
        pygame.draw.rect(screen, (255, 255, 255), rect)
        width_value_surface = font.render(str(global_var.WIDTH), True, (0, 70, 67), (255,255,255))
        text_rect = width_value_surface.get_rect()
        text_rect.center = rect.center
        screen.blit(width_value_surface, text_rect)

        #back
        back_button_image = pygame.image.load("./assets/pictures/back_button.png")
        original_width, original_height = back_button_image.get_size()
        scale_factor = SCREENWIDTH / 2900
        new_width = int(original_width * scale_factor)
        new_height = int(original_height * scale_factor)
        back_button_resized = pygame.transform.smoothscale(back_button_image, (new_width, new_height))
        back_button_rect = back_button_resized.get_rect(topleft=(2 * SCREENWIDTH / 20, 15 * SCREENHEIGHT / 20))
        screen.blit(back_button_resized, back_button_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if sound_plus_button.is_clicked(event):
                    new_value = volume + (MAX_VOLUME - MIN_VOLUME) / 9
                    volume = min(new_value, MAX_VOLUME)
                if sound_minus_button.is_clicked(event):
                    new_value = volume - (MAX_VOLUME - MIN_VOLUME) / 9
                    volume = max(new_value, MIN_VOLUME)
                if speed_plus_button.is_clicked(event):
                    new_value = global_var.SPEED + (MAX_SPEED - MIN_SPEED) / 9
                    global_var.SPEED = min(new_value, MAX_SPEED)
                if speed_minus_button.is_clicked(event):
                    new_value = global_var.SPEED - (MAX_SPEED - MIN_SPEED) / 9
                    global_var.SPEED = max(new_value, MIN_VOLUME)
                if width_plus_button.is_clicked(event):
                    new_value = global_var.WIDTH + 1
                    global_var.WIDTH = min(new_value, MAX_WIDTH)
                if width_minus_button.is_clicked(event):
                    new_value = global_var.WIDTH - 1
                    global_var.WIDTH = max(new_value, MIN_WIDTH)
                if back_button_rect.collidepoint(event.pos):
                    return




        pygame.display.flip()


