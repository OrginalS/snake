from time import sleep
import pygame

from settings import Settings
from snake import Snake
from fruit import Fruit


class SnakeGame:
    """overall class to manage game assets and behavior"""

    def __init__(self):
        """initialize the game, and create game resources"""

        pygame.init()

        # settings
        self.settings = Settings()

        # screen
        self.screen = pygame.display.set_mode(self.settings.screen_size)
        pygame.display.set_caption("Snake")

        # objects
        self.snake = Snake(self)
        self.fruit = Fruit(self)

        # lines
        self.lines = [i * self.settings.block for i in range(self.screen.get_rect().right // self.settings.block)]

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                self._check_key_presses(event)

    def _check_key_presses(self, event):
        """Decides what to do when a button is pressed"""
        if event.key == pygame.K_UP:
            self.snake.move("UP")
        elif event.key == pygame.K_DOWN:
            self.snake.move("DOWN")
        elif event.key == pygame.K_LEFT:
            self.snake.move("LEFT")
        elif event.key == pygame.K_RIGHT:
            self.snake.move("RIGHT")
        elif event.key == pygame.K_ESCAPE:
            exit()

    def _lines(self):
        """Draws dividing lines"""
        for line in self.lines:
            pygame.draw.line(self.screen, (0, 0, 0), (0, line), (self.settings.screen_size[0], line))
            pygame.draw.line(self.screen, (0, 0, 0), (line, 0), (line, self.settings.screen_size[1]))

    def _update_snake(self):
        """Moves the snake"""
        self.snake.head[0] += self.snake.movement[0]
        self.snake.head[1] += self.snake.movement[1]

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""

        # fill the screen with color
        self.screen.fill(self.settings.bg_color)

        # draw fruit
        pygame.draw.rect(self.screen, self.fruit.color, (self.fruit.fruits, self.fruit.block))

        # draw snake
        pygame.draw.rect(self.screen, self.snake.color, (self.snake.head, self.snake.block))
        for part in self.snake.body:
            pygame.draw.rect(self.screen, self.snake.color, (part, self.snake.block))

        # draw lines
        self._lines()
        pygame.display.flip()
        sleep(0.2)

    def run(self):
        """Starts the game"""
        while True:
            if not self.fruit.fruits:
                self.fruit.new_fruit()
                print("fruit")
            self._check_events()
            self._update_snake()
            self._update_screen()


if __name__ == "__main__":
    sg = SnakeGame()
    sg.run()
