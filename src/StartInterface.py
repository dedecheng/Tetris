from turtledemo.nim import SCREENWIDTH

from Button import Button
import pygame, sys

from main import bord_width

# initialize
pygame.init()
pygame.mixer.init()

#screen size
SCREENWIDTH = 720
SCREENHEIGHT = 540
SCREEN = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))

# import images
BG = pygame.image.load("../assets/BG.png")
TITLE = pygame.image.load("../assets/TETRIS.png")
QUIT_BUTTON = pygame.image.load("../assets/QuitButton.png")
ELLIPSE = pygame.image.load("../assets/BGasset.png")

# import music
pygame.mixer.music.load("../assets/BGmusic.mp3")
pygame.mixer.music.play(-1)

# scale image
new_width = SCREENWIDTH * 0.92
new_height = SCREENHEIGHT * 0.87
SMALL_BG = pygame.transform.smoothscale(BG, (new_width, new_height))

new_width = TITLE.get_width() * 0.5
new_height = TITLE.get_height() * 0.5
SMALL_TITLE = pygame.transform.smoothscale(TITLE, (new_width, new_height))

new_width = ELLIPSE.get_width() * 0.5
new_height = ELLIPSE.get_height() * 0.5
SMALL_ELLIPSE = pygame.transform.smoothscale(ELLIPSE, (new_width, new_height))

new_width = QUIT_BUTTON.get_width() * 0.5
new_height = QUIT_BUTTON.get_height() * 0.5
SMALL_QUIT = pygame.transform.smoothscale(QUIT_BUTTON, (new_width, new_height))



# setting font
def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font(pygame.font.match_font('arial'), size)


def play():
    while True:


        pygame.display.update()


def options():
    while True:


        pygame.display.update()


def main_menu():
    while True:
        SCREEN.fill((43, 97, 105))
        BG_x = (SCREENWIDTH - SMALL_BG.get_width()) // 2
        BG_y = (SCREENHEIGHT - SMALL_BG.get_height()) // 2
        SCREEN.blit(SMALL_BG, (BG_x, BG_y))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        #place images: title, ellipse, quit
        image_width, image_height = SMALL_TITLE.get_size()
        
        title_x = (SCREENWIDTH - image_width)//2
        title_y = SCREENHEIGHT - (SCREENHEIGHT//2 + image_height)

        SCREEN.blit(SMALL_TITLE, (title_x, title_y))
        SCREEN.blit(SMALL_ELLIPSE, (0, SCREENHEIGHT - SMALL_ELLIPSE.get_height()))

        SCREEN.blit(SMALL_QUIT, (SCREENWIDTH * 0.87, SCREENHEIGHT - SMALL_QUIT.get_height() * 1.5))

        # button start
        pygame.draw.rect(SCREEN, (225, 97, 98), (150, 280, 150, 90), border_radius = 100)
        # button option
        pygame.draw.ellipse(SCREEN, (249, 188, 96), (380, 280, 90, 90))
        # button rank
        pygame.draw.ellipse(SCREEN, (43, 97, 105), (480, 280, 90, 90))
        # button quit

        PLAY_BUTTON = Button(150, 100, 100, 50, "START", get_font(30), "#E16162", "#2B6169", "#FFFFFF")
        QUIT_BUTTON = Button(250, 100, 100, 50, "QUIT", get_font(30), "#2B6169", "#F9BC60", "#FFFFFF")


        for button in [PLAY_BUTTON]:
            button.change_color(MENU_MOUSE_POS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.check_Input(MENU_MOUSE_POS):
                    play()

                if QUIT_BUTTON.check_Input(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


main_menu()