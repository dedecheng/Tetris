import pygame

# setting font
def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font(pygame.font.match_font("../assets/STHupo.ttf"), size)

class Button:
    def __init__(self, x, y, width, height, text, font, bg_color, text_color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.bg_color = bg_color
        self.text_color = text_color
        self.hover_color = hover_color

    def draw(self, screen):
        # 獲取滑鼠位置
        mouse_pos = pygame.mouse.get_pos()

        # 如果滑鼠懸停，改變顏色
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.bg_color, self.rect)

        # 繪製文字
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        # 偵測滑鼠按下事件
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):  # 左鍵點擊
                return True
        return False