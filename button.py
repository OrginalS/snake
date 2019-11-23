import pygame
import pygame.font


class Button:
    """Button class"""

    def __init__(self, snake_game, color, text, pos):
        self.snake_game = snake_game
        self.size = (100, 40)
        self.color = color
        self.text = text
        self.pos = pos
        self.font = pygame.font.SysFont(None, 36)

    def show_button(self):
        """Shows button on the screen"""
        pygame.draw.rect(self.snake_game.screen, self.color, (self.pos, self.size))
