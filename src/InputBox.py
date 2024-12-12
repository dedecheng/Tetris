import pygame, sys

pygame.init()

# setting font
def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font(pygame.font.match_font("../assets/STHupo.ttf"), size)

class InputBox():
    def __init__(self, x, y, width, height, font, text_color, box_color, active_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = box_color
        self.active_color = active_color
        self.text_color = text_color
        self.font = font
        self.active = False
        self.text = ""
        self.cursor_visible = True
        self.cursor_timer = 0

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If mouse click inside the input box, activate it
            if self.rect.collidepoint(event.pos):
                self.active = True  # Activate the input box
            else:
                self.active = False  # Deactivate if clicked outside
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]   # Delete last character
            elif event.key == pygame.K_RETURN:  # enter to confirm input
                return self.text
            else:
                self.text += event.unicode
        return None

    def draw(self, screen):
        # Draw input box
        color = self.active_color if self.active else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=5)

        # Draw text
        text_surface = self.font.render(self.text, True, self.text_color)
        screen.blit(text_surface, (self.rect.x + 10, self.rect.y + (self.rect.height - text_surface.get_height()) // 2))

        # Draw cursor
        if self.active and self.cursor_visible:
            cursor_x = self.rect.x + 10 + text_surface.get_width()
            cursor_y = self.rect.y + 5
            cursor_height = self.rect.height - 10
            pygame.draw.rect(screen, self.text_color, (cursor_x, cursor_y, 2, cursor_height))

    def update(self):
        # Cursor blink
        self.cursor_timer += 1
        if self.cursor_timer >= 30:  # Toggle visibility every 30 frames
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0