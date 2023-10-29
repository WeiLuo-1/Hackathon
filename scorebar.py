import pygame
from constants import screen_width, screen_height

class ScoreBar:
    def __init__(self):
        self.human_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont('Arial', 30)
        self.human_color = (0, 255, 0)  # Green
        self.ai_color = (255, 0, 0)    # Red

    def increase_human_score(self):
        self.human_score += 1

    def increase_ai_score(self):
        self.ai_score += 1

    def reset(self):
        self.human_score = 0
        self.ai_score = 0

    def draw(self, window):
        human_text = self.font.render(f'Human: {self.human_score}', True, self.human_color)
        ai_text = self.font.render(f'AI: {self.ai_score}', True, self.ai_color)

        window.blit(human_text, (10, screen_height - 40))
        window.blit(ai_text, (screen_width - ai_text.get_width() - 10, screen_height - 40))
