from turtledemo.nim import SCREENWIDTH

from Button import Button
import pygame, sys

pygame.init()

#screen size
SCREENWIDTH = 720
SCREENHEIGHT = 540

SCREEN = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))

# import images
BG = pygame.image.load("../assets/Background.png")

TITLE = pygame.image.load("../assets/TETRIS.png")
TITLE_width, TITLE_height = TITLE.get_size()

# scale title image
new_width = TITLE_width * 0.5
new_height = TITLE_height * 0.5
SMALL_TITLE = pygame.transform.smoothscale(TITLE, (new_width, new_height))

ELLIPSE = pygame.image.load("../assets/Ellipse.png")
new_width = ELLIPSE.get_width() * 0.5
new_height = ELLIPSE.get_height() * 0.5
SMALL_ELLIPSE = pygame.transform.smoothscale(ELLIPSE, (new_width, new_height))

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
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        #place images: title, ellipse
        image_width, image_height = SMALL_TITLE.get_size()
        
        title_x = (SCREENWIDTH - image_width)//2
        title_y = SCREENHEIGHT - (SCREENHEIGHT//2 + image_height)

        SCREEN.blit(SMALL_TITLE, (title_x, title_y))
        SCREEN.blit(SMALL_ELLIPSE, (0, SCREENHEIGHT - SMALL_ELLIPSE.get_height()))

        # button start
        pygame.draw.rect(SCREEN, (225, 97, 98), (120, 300, 150, 90), border_radius = 100)
        # button option

        # button rank

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