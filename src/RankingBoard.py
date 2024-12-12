import pygame
import json
from pathlib import Path
import sys

class RankingBoard:
    def __init__(self):
        root_dir = Path(__file__).parent.parent
        self.screen = pygame.display.set_mode((800, 600))
        self.font = pygame.font.SysFont("Calibri Light", 24)
        self.ranking_file = str(root_dir) + r".\assets\ranking_board.json"  # 文件名更新為 RankingBoard.json
        self.rankings = self.load_rankings()

        # 加載背景與按鈕
        self.bg_image = pygame.image.load(str(root_dir) + r'.\assets\ranking_bg.png')  # 排行榜背景
        self.back_button_image = pygame.image.load(str(root_dir) + r".\assets\back_button.png")  # 返回按鈕圖片
        self.back_button_rect = self.back_button_image.get_rect(topleft=(50, 50))

    def load_rankings(self):
        # 從 JSON 文件加載排行榜數據
        try:
            with open(self.ranking_file, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            # 如果文件不存在，返回空列表
            return []
        except json.JSONDecodeError:
            # 如果 JSON 格式錯誤，返回空列表
            return []

    def save_rankings(self, player_name, player_score):
        # 新增玩家數據
        new_entry = {"name": player_name, "score": player_score, "line": self.line_cleared}  # 注意score和line是int
        self.rankings.append(new_entry)

        # 排序排行榜數據（根據分數從高到低）
        self.rankings.sort(key=lambda x: x["score"], reverse=True)

        # 保存到 JSON 文件
        with open(self.ranking_file, "w", encoding="utf-8") as file:
            json.dump(self.rankings, file, ensure_ascii=False, indent=4)



    def render(self):
        screen = pygame.display.set_mode((800, 600))
        while True:
            # 清空畫布，繪製背景
            self.screen.fill((0, 0, 0))  # 清除畫布（黑色背景）
            bg_resized = pygame.transform.scale(self.bg_image, (self.screen.get_width(), self.screen.get_height()))
            self.screen.blit(bg_resized, (0, 0))

            # 繪製返回按鈕
            original_width, original_height = self.back_button_image.get_size()
            scale_factor = 0.25
            new_width = int(original_width * scale_factor)
            new_height = int(original_height * scale_factor)
            back_button_resized = pygame.transform.smoothscale(self.back_button_image, (new_width, new_height))
            back_button_rect = back_button_resized.get_rect(topleft=(50, 30))
            self.screen.blit(back_button_resized, back_button_rect)

            # 繪製排行榜數據
            for idx, entry in enumerate(self.rankings):
                if idx >= 8:
                    break
                row_font = pygame.font.Font(None, 30)
                name = entry["name"]
                line = entry["line"]
                score = entry["score"]

                # 繪製玩家名稱、行數和分數，刪除序列號，調整 X 座標位置
                name_surface = row_font.render(name, True, (0, 0, 0))
                line_surface = row_font.render(str(line), True, (0, 0, 0))
                score_surface = row_font.render(str(score), True, (0, 0, 0))

                # 調整行距間隔，避免重疊
                y_position = 212 + idx * 39.75
                self.screen.blit(name_surface, (180, y_position))  # 調整名稱的位置
                self.screen.blit(line_surface, (380, y_position))  # 調整行數的位置
                self.screen.blit(score_surface, (570, y_position))  # 調整分數的位置

            # event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button_rect.collidepoint(event.pos):
                        return

            pygame.display.update()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 檢查是否點擊了返回按建
            if self.back_button_rect.collidepoint(event.pos):
                return "back"  # 返回首頁
        return None


# 測試用
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("排行榜展示")
    clock = pygame.time.Clock()

    ranking_board = RankingBoard()

    running = True
    while running:
        screen.fill((255, 255, 255))
        ranking_board.render()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            ranking_board.handle_event(event)

        clock.tick(60)

    pygame.quit()
