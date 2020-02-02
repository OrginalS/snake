import pygame.font


class Score:
    """Score class"""

    def __init__(self, snake_game):
        """Initialize score class"""

        self.snake_game = snake_game
        self.score = 0
        try:
            with open("highscore.txt", "r") as f:
                self.high_score = int(f.readline())
        except (FileNotFoundError, ValueError):
            self.high_score = 0

    def save_high_score(self):
        """Saves high score"""

        if not self.snake_game.settings.ai_enabled:
            with open("highscore.txt", "w") as f:
                if self.score > self.high_score:
                    self.high_score = self.score
                    f.write(str(self.high_score))
                else:
                    f.write(str(self.high_score))

    def show_score(self, pause=False):
        """Shows score and high score on the screen"""

        font = pygame.font.SysFont(None, 48)
        score_image = font.render(f"SCORE: {self.score}", True, (0, 0, 0))
        high_score_image = font.render(f"HIGH SCORE: {self.high_score}", True, (0, 0, 0))
        if pause:
            self.snake_game.screen.blit(score_image, (225, 225))
        else:
            self.snake_game.screen.blit(score_image, (225, 300))
            self.snake_game.screen.blit(high_score_image, (175, 250))
