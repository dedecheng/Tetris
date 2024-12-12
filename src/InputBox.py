import pygame, sys

#screen size
SCREENWIDTH = 720
SCREENHEIGHT = 540

pygame.init()


# setting font
def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font(pygame.font.match_font("../assets/font/comic.ttf"), size)

class InputBox():
    def __init__(self, x, y, width, height, font, text_color, box_color, active_color, label=""):
        self.full_rect = pygame.Rect(x, y, width, height)
        self.color = box_color
        self.active_color = active_color
        self.text_color = text_color
        self.font = font
        self.active = False
        self.text = ""
        self.cursor_visible = True
        self.cursor_timer = 0
        self.label = label  # Add label attribute for instructions
        self.label_font = get_font(30)
        # input box
        self.rect = pygame.Rect(x + 30, y + height * 0.5, width * 0.8, height * 0.2)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If mouse click inside the input box, activate it
            if self.rect.collidepoint(event.pos):
                self.active = True  # Activate the input box
            else:
                self.active = False  # Deactivate if clicked outside
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]  # Delete last character
            elif event.key == pygame.K_RETURN:  # enter to confirm input
                return self.text
            else:
                self.text += event.unicode
        return None

    def draw(self, screen):
        # Draw the larger background rectangle that contains the input box and the label
        pygame.draw.rect(screen, "#FFFFFF", (self.full_rect.x - 10, self.full_rect.y - 10, self.full_rect.width + 20, self.full_rect.height + 20), border_radius = 10)
        pygame.draw.rect(screen, "#6BAEB9", self.full_rect, border_radius = 10)
        # Draw the label (instruction) text above the input box
        if self.label:
            label_surface = self.label_font.render(self.label, True, self.text_color)
            screen.blit(label_surface, (self.full_rect.x + 30,
                                        self.full_rect.y + 30))  # Place the label above the input box

        # Draw input box
        color = self.active_color if self.active else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=5)

        # Draw text inside the input box
        text_surface = self.font.render(self.text, True, self.text_color)
        screen.blit(text_surface, (self.rect.x + 10, self.rect.y + (self.rect.height - text_surface.get_height()) // 2))

        # Draw cursor
        if self.active and self.cursor_visible:
            cursor_x = self.rect.x + 10 + text_surface.get_width()
            cursor_y = self.rect.y + 5
            cursor_height = self.rect.height - 6
            pygame.draw.rect(screen, self.text_color, (cursor_x, cursor_y, 2, cursor_height))

    def update(self):
        # Cursor blink
        self.cursor_timer += 1
        if self.cursor_timer >= 30:  # Toggle visibility every 30 frames
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0