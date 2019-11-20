class Snake:
    """Snake"""

    def __init__(self, snake_game):
        self.snake_game = snake_game
        self.block = (self.snake_game.settings.block, self.snake_game.settings.block)
        self.size = 1
        self.color = (255, 255, 255)
        self.head = [
            self.snake_game.settings.screen_size[0] // self.block[0] // 2 * self.block[0],
            self.snake_game.settings.screen_size[1] // self.block[1] // 2 * self.block[1]
        ]
        self.body = []
        self.movement = [0, 0]

    def move(self, direction):
        if direction == "DOWN":
            self.movement = [0, self.block[1]]
        elif direction == "UP":
            self.movement = [0, self.block[1] * -1]
        elif direction == "RIGHT":
            self.movement = [self.block[0], 0]
        elif direction == "LEFT":
            self.movement = [self.block[0] * -1, 0]

