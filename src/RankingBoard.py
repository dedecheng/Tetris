import pygame
import json

class RankingBoard:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 24)
        self.ranking_file = "assets/RankingBoard.json"  # 文件名更新為 RankingBoard.json
        self.rankings = self.load_rankings()

        # 加載背景與按鈕
        self.bg_image = pygame.image.load("assets/ranking_bg.png")  # 排行榜背景
        self.back_button_image = pygame.image.load("assets/back_button.png")  # 返回按鈕圖片
        self.back_button_rect = self.back_button_image.get_rect(topleft=(50, 50))

    def load_rankings(self):
        #從 JSON 文件加載排行榜數據
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
        new_entry = {"name": player_name, "score": player_score, "line": self.line_cleared} # 注意score和line是int
        self.rankings.append(new_entry)

        # 排序排行榜數據（根據分數從高到低）
        self.rankings.sort(key=lambda x: x["score"], reverse=True)

        # 保存到 JSON 文件
        with open(self.ranking_file, "w", encoding="utf-8") as file:
            json.dump(self.rankings, file, ensure_ascii=False, indent=4)



    def render(self):
        # 繪製背景和標題(大小不確定，可能要再調) 
        self.screen.blit(self.bg_image, (0, 0))
        self.screen.blit(self.back_button_image, self.back_button_rect)

        title_surface = self.font.render("Ranking", True, (0, 0, 0))
        self.screen.blit(title_surface, (self.screen.get_width() // 2 - 50, 20))

        # 繪製排行榜數據(大小不確定，可能要再調) 
        header_surface = self.font.render("Name       Lines Cleared       Score", True, (0, 0, 0))
        self.screen.blit(header_surface, (100, 100))

        for idx, entry in enumerate(self.rankings):
            name = entry["name"]
            line = entry["line"]
            score = entry["score"]

            # 玩家數據
            name_surface = self.font.render(f"{idx + 1}. {name}", True, (0, 0, 0))
            line_surface = self.font.render(str(line), True, (0, 0, 0))
            score_surface = self.font.render(str(score), True, (0, 0, 0))

            self.screen.blit(name_surface, (100, 140 + idx * 30))
            self.screen.blit(line_surface, (300, 140 + idx * 30))
            self.screen.blit(score_surface, (450, 140 + idx * 30))



    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 檢查是否點擊了返回按建
            if self.back_button_rect.collidepoint(event.pos):
                return "back"  # 返回首頁
        return None
