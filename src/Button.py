import pygame, math

pygame.mixer.init()

# setting font
def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font(pygame.font.match_font("../assets/font/STHupo.ttf"), size)

class Button:
    click_sound = pygame.mixer.Sound("../assets/music/button-click.wav")
    click_sound.set_volume(1.2)

    def __init__(self, x, y, width, height, text, font, color, hover_color, text_color):
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.rect = pygame.Rect(x, y, width, height)
        self.is_hovered = False

    def draw(self, screen):
        # Check if the mouse is hovered over the button
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(mouse_pos)

        # Draw the button with color change on hover
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect)

        # Draw the text centered in the button
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.click_sound:
                    self.click_sound.play()
                return True
        return False

class RectButton(Button):
    def __init__(self, x, y, width, height, text, font, color, hover_color, text_color):
        super().__init__(x, y, width, height, text, font, color, hover_color, text_color)
    def draw(self, screen):
        # Check if the mouse is hovered over the button
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(mouse_pos)

        # Draw the button with color change on hover
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=100)

        # Draw the text centered in the button
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

class CircleButton(Button):
    def __init__(self, x, y, radius, text, font, color, hover_color, text_color):
        # For CircleButton, we store a radius instead of width/height
        self.radius = radius
        super().__init__(x - radius, y - radius, 2*radius, 2*radius, text, font, color, hover_color, text_color)

    def draw(self, screen):
        # Check if the mouse is hovered over the button
        mouse_pos = pygame.mouse.get_pos()
        distance = math.dist(mouse_pos, (self.rect.centerx, self.rect.centery))
        self.is_hovered = distance <= self.radius

        # Draw the button with color change on hover
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.circle(screen, color, (self.rect.centerx, self.rect.centery), self.radius)

        # Draw the text centered in the button
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=(self.rect.centerx, self.rect.centery))
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.click_sound:
                self.click_sound.play()
            distance = math.dist(event.pos, (self.rect.centerx, self.rect.centery))
            return distance <= self.radius
        return False
