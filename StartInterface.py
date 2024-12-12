from src.Button import Button, RectButton, CircleButton
import pygame, sys
from src.GameWindow import game_loop
from src.RankingBoard import RankingBoard

# initialize
pygame.init()
pygame.mixer.init()

#screen size
SCREENWIDTH = 720
SCREENHEIGHT = 540
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))

# import images
BG = pygame.image.load("assets/BG.png")
TITLE = pygame.image.load("assets/TETRIS.png")
QUIT_BUTTON = pygame.image.load("assets/QuitButton.png")
BGassets = pygame.image.load("assets/BGasset.png")
MOUSE_IMAGE = pygame.image.load("assets/mouse.png")

# import music
pygame.mixer.music.load("assets/BGmusic.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.2)

# scale image
new_width = SCREENWIDTH * 0.92
new_height = SCREENHEIGHT * 0.87
SMALL_BG = pygame.transform.smoothscale(BG, (new_width, new_height))

new_width = TITLE.get_width() * 0.5
new_height = TITLE.get_height() * 0.5
SMALL_TITLE = pygame.transform.smoothscale(TITLE, (new_width, new_height))

new_width = BGassets.get_width() * 0.5
new_height = BGassets.get_height() * 0.5
SMALL_ELLIPSE = pygame.transform.smoothscale(BGassets, (new_width, new_height))

new_width = QUIT_BUTTON.get_width() * 0.5
new_height = QUIT_BUTTON.get_height() * 0.5
SMALL_QUIT = pygame.transform.smoothscale(QUIT_BUTTON, (new_width, new_height))

ranking_board = RankingBoard()
# setting font
def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font(pygame.font.match_font('arialblack'), size)

def play():
    game_loop()
    # while True:
    #     SCREEN.fill("#2B6169")
    #     pygame.display.update()

def options():
    while True:
        pygame.display.update()

def main_menu():
    SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    # Create buttons
    START_BTN = RectButton(150, 280, 150, 90, "START", get_font(25), "#2B6169", "#E16162", "#FFFFFF")
    QUIT_BTN = CircleButton(SCREENWIDTH * 0.87, SCREENHEIGHT - SMALL_QUIT.get_height() * 1.5, 50, "QUIT", get_font(30),
                            "#2B6169", "#E16162", "#FFFFFF")
    RANK_BTN = CircleButton(425, 325, 45, "RANK", get_font(25), "#2B6169", "#F9BC60", "#FFFFFF")
    OPTION_BTN =  CircleButton(525, 325, 45, "SET", get_font(25), "#2B6169", "#30AB3D", "#FFFFFF")

    while True:
        SCREEN.fill((43, 97, 105))

        # Background and title position
        BG_x = (SCREENWIDTH - SMALL_BG.get_width()) // 2
        BG_y = (SCREENHEIGHT - SMALL_BG.get_height()) // 2
        SCREEN.blit(SMALL_BG, (BG_x, BG_y))

        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MENU_MOUSE_RECT = (MENU_MOUSE_POS[0] - 0.8 *MOUSE_IMAGE.get_width(), MENU_MOUSE_POS[1] - 0.75*MOUSE_IMAGE.get_height())


        # Place images: title, ellipse, quit
        image_width, image_height = SMALL_TITLE.get_size()
        title_x = (SCREENWIDTH - image_width) // 2
        title_y = SCREENHEIGHT - (SCREENHEIGHT // 2 + image_height)

        SCREEN.blit(SMALL_TITLE, (title_x, title_y))
        SCREEN.blit(SMALL_ELLIPSE, (0, SCREENHEIGHT - SMALL_ELLIPSE.get_height()))
        SCREEN.blit(SMALL_QUIT, (SCREENWIDTH * 0.87, SCREENHEIGHT - SMALL_QUIT.get_height() * 1.5))

        # Draw buttons manually if not using button classes (comment this part if using classes)
        pygame.draw.rect(SCREEN, (225, 97, 98), (150, 280, 150, 90), border_radius=100)  # Start button
        pygame.draw.ellipse(SCREEN, (249, 188, 96), (380, 280, 90, 90))  # Option button
        pygame.draw.ellipse(SCREEN, (43, 97, 105), (480, 280, 90, 90))  # Rank button

        # Draw the buttons (Rect and Circle buttons)
        START_BTN.draw(SCREEN)
        QUIT_BTN.draw(SCREEN)
        OPTION_BTN.draw(SCREEN)
        RANK_BTN.draw(SCREEN)
        SCREEN.blit(MOUSE_IMAGE, MENU_MOUSE_RECT)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if START_BTN.is_clicked(event):
                    play()
                if RANK_BTN.is_clicked(event):
                    ranking_board.render()
                    SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
                if QUIT_BTN.is_clicked(event):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

if __name__ == "__main__":
    main_menu()
