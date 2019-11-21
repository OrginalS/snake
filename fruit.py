from random import randint


class Fruit:
    """Fruit"""

    def __init__(self, snake_game):
        self.snake_game = snake_game
        self.screen = self.snake_game.screen.get_rect()
        self.block = (self.snake_game.settings.block, self.snake_game.settings.block)
        self.size = 1
        self.color = (255, 0, 0)
        self.fruits = []
        self.new_fruit()

    def new_fruit(self):
        """Generates new fruit if there is no fruit on the screen"""
        x = self.screen[2] / self.block[0]
        y = self.screen[3] / self.block[1]
        self.fruits.append([randint(0, x-1) * self.block[0], randint(0, y-1) * self.block[1]])
