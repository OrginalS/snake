import pygame
import pygame.font


class Button:
    """Button class"""

    def __init__(self, snake_game, color, text, pos, size, font):
        self.snake_game = snake_game

        # button properties
        self.color = color
        self.text = text
        self.pos = pos
        self.size = size
        self.font = pygame.font.SysFont(None, font)
        self.font_color = (255, 255, 255)

        # build buttons rect object and center it
        self.rect = pygame.Rect(*self.pos, *self.size)

        # prep text
        self._prep_text(self.text)

    def _prep_text(self, text):
        """Turn msg into a rendered image and center text on the button."""
        self.text_image = self.font.render(text, True, self.font_color, self.color)
        self.text_image_rect = self.text_image.get_rect()
        self.text_image_rect.center = self.rect.center

    def show_button(self):
        """Shows button on the screen"""
        # draw blank button and then draw message
        self.snake_game.screen.fill(self.color, self.rect)
        self._prep_text(self.text)
        self.snake_game.screen.blit(self.text_image, self.text_image_rect)
