import pygame, math, sys

# setting font
def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font(pygame.font.match_font("../assets/STHupo.ttf"), size)

class Button:
    def __init__(self, text, font, color, hover_color, text_color):
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False

    def draw(self, screen):
        raise NotImplementedError("子類別必須實現 draw 方法！")

    def is_clicked(self, event):
        raise NotImplementedError("子類別必須實現 is_clicked 方法！")

class RectButton(Button):
    def __init__(self, x, y, width, height, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        # 檢查滑鼠是否懸停
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(mouse_pos)

        # 繪製按鈕
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect)

        # 繪製文字
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(event.pos)
        return False

class CircleButton(Button):
    def __init__(self, x, y, radius, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.x = x
        self.y = y
        self.radius = radius

    def draw(self, screen):
        # 檢查滑鼠是否懸停
        mouse_pos = pygame.mouse.get_pos()
        distance = math.dist(mouse_pos, (self.x, self.y))
        self.is_hovered = distance <= self.radius

        # 繪製按鈕
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.circle(screen, color, (self.x, self.y), self.radius)

        # 繪製文字
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=(self.x, self.y))
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            distance = math.dist(event.pos, (self.x, self.y))
            return distance <= self.radius
        return False
