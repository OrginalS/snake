class AI:
    """Artificial intelligence"""

    def __init__(self, snake_game):
        self.snake_game = snake_game
        self.pos = self.snake_game.snake.head
        self.next_move = 0
        self.start = 1
        self.block = self.snake_game.settings.block

    def ai_move(self):
        if self.start:
            self.snake_game.snake.move("RIGHT")
            self.start = 0
        elif self.next_move:
            self.snake_game.snake.move(self.next_move)
            self.next_move = 0
        elif self.pos[0] == 0 and self.pos[1] == 0 + self.block:
            self.start = 1
        elif self.pos[1] == self.snake_game.settings.screen_size[1] - self.block:
            self.snake_game.snake.move("LEFT")
            self.next_move = "UP"
        elif self.pos[0] == self.snake_game.settings.screen_size[0] - self.block:
            self.snake_game.snake.move("DOWN")
        elif self.pos[1] == 0 + self.snake_game.settings.block:
            self.snake_game.snake.move("LEFT")
            self.next_move = "DOWN"


