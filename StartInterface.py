from math import radians

from src.Button import Button, RectButton, CircleButton
from src.InputBox import InputBox
import pygame, sys
from src.GameWindow import game_loop
from src.RankingBoard import RankingBoard
from src.setting import setting_page
import src.global_var as global_var

# initialize
pygame.init()
pygame.mixer.init()

#screen size
SCREENWIDTH = 720
SCREENHEIGHT = 540
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))

# import images
BG = pygame.image.load("./assets/pictures/BG.png")
TITLE = pygame.image.load("./assets/pictures/TETRIS.png")
QUIT_BUTTON = pygame.image.load("./assets/pictures/QuitButton.png")
BGassets = pygame.image.load("./assets/pictures/BGasset.png")
MOUSE_IMAGE = pygame.image.load("./assets/pictures/mouse.png")

# import music
pygame.mixer.music.load("./assets/music/BGmusic.mp3")
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

# setting font
def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font(pygame.font.match_font('arialblack'), size)

def play():
    game_loop()
    # while True:
    #     SCREEN.fill("#2B6169")
    #     pygame.display.update()



def main_menu():
    SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    clock = pygame.time.Clock()
    player_name = None
    show_input_box = False

    # Create buttons
    START_BTN = RectButton(150, 280, 150, 90, "START", get_font(25), "#2B6169", "#E16162", "#FFFFFF")
    QUIT_BTN = CircleButton(SCREENWIDTH * 0.906, SCREENHEIGHT - SMALL_QUIT.get_height() * 1, 30, "", get_font(30),
                            "#6BAEB9", "#2B6169", "#FFFFFF")
    RANK_BTN = CircleButton(425, 325, 45, "RANK", get_font(25), "#2B6169", "#F9BC60", "#FFFFFF")
    OPTION_BTN =  CircleButton(525, 325, 45, "SET", get_font(25), "#2B6169", "#30AB3D", "#FFFFFF")
    input_x = (SCREENWIDTH - 300) // 2
    input_y = (SCREENHEIGHT - 120) // 2
    # input box
    INPUT_BOX = InputBox(input_x, input_y, width=300, height=120, font=get_font(20), text_color="#004643", box_color="#D9D9D9",
                         active_color="#FFFFFF", label="Insert your name:")

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
        QUIT_BTN.draw(SCREEN)
        SCREEN.blit(SMALL_QUIT, (SCREENWIDTH * 0.87, SCREENHEIGHT - SMALL_QUIT.get_height() * 1.5))

        # Draw the buttons (Rect and Circle buttons)
        START_BTN.draw(SCREEN)
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
                    show_input_box = True
                if RANK_BTN.is_clicked(event):
                    ranking_board = RankingBoard()
                    ranking_board.render()
                    SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
                if OPTION_BTN.is_clicked(event):
                    setting_page()
                    SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
                if QUIT_BTN.is_clicked(event):
                    pygame.quit()
                    sys.exit()

            if show_input_box:
                # Handle player name input
                name = INPUT_BOX.handle_event(event)
                if name:
                    global_var.PLAYER_NAME = name
                    play()  # Start the game after input is complete
                    show_input_box = False
                    SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))

        if show_input_box:
            INPUT_BOX.update()
            INPUT_BOX.draw(SCREEN)

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main_menu()
