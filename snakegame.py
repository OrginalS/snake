from time import sleep
import pygame

from settings import Settings
from snake import Snake
from fruit import Fruit
from ai import AI
from button import Button


class SnakeGame:
    """Overall class to manage game assets and behavior"""

    def __init__(self):
        """Initialize the game, and create game resources"""

        pygame.init()

        # settings
        self.settings = Settings()

        # logo
        self.logo = pygame.image.load("images/logo.png")

        # actives
        self.game_active = False
        self.settings_button_active = False

        # screen
        self.screen = pygame.display.set_mode(self.settings.screen_size)
        pygame.display.set_caption("Snake")

        # objects
        self.snake = Snake(self)
        self.fruit = Fruit(self)
        self.ai = AI(self)

        # lines
        self.lines = [i * self.settings.block for i in range(self.screen.get_rect().right // self.settings.block)]

        # buttons
        self.play_button = Button(
            self, (0, 100, 0), "PLAY", [i-j for i, j in zip(self.screen.get_rect().center, (50, 20))], (100, 40), 36
        )
        self.settings_button = Button(
            self, (0, 0, 0), "SETTINGS", (self.play_button.pos[0]-25, self.play_button.pos[1] + 100), (150, 40), 36
        )
        self.back_button = Button(
            self, (0, 0, 0), "BACK", (self.play_button.pos[0], self.play_button.pos[1] + 100), (100, 40), 36
        )
        self.ai_button = Button(
            self, (200, 0, 0), "AI DISABLED", (self.play_button.pos[0]-40, self.play_button.pos[1]), (180, 40), 36
        )

    def _reset_game(self):
        """Resets the game"""
        self.__init__()

    def _check_events(self):
        """Handles events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                self._check_key_presses(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._check_mouse_clicks(event)

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

    def _check_mouse_clicks(self, event):
        """Handles mouse actions"""
        if event.button == 1 and not self.game_active:
            # main screen buttons
            if not self.settings_button_active:
                # play button
                if self.play_button.rect.collidepoint(*event.pos):
                    self.game_active = True
                # settings button
                elif self.settings_button.rect.collidepoint(*event.pos):
                    self.settings_button_active = True
            # setting screen buttons
            elif self.settings_button_active:
                # back button
                if self.back_button.rect.collidepoint(*event.pos):
                    self.settings_button_active = False
                    # ai button
                elif self.ai_button.rect.collidepoint(*event.pos):
                    if self.settings.ai_enabled:
                        self.ai_button.color = (200, 0, 0)
                        self.ai_button.text = "AI DISABLED"
                        self.settings.ai_enabled = False
                    elif not self.settings.ai_enabled:
                        self.ai_button.color = (0, 200, 0)
                        self.ai_button.text = "AI ENABLED"
                        self.settings.ai_enabled = True

            # todo: dark mode button, sound button, line button, reset button

    def _lines(self):
        """Draws dividing lines"""
        for line in self.lines:
            pygame.draw.line(self.screen, (0, 0, 0), (0, line), (self.settings.screen_size[0], line))
            pygame.draw.line(self.screen, (0, 0, 0), (line, 0), (line, self.settings.screen_size[1]))

    def _update_snake(self):
        """Moves the snake"""
        self.snake.head[0] += self.snake.movement[0]
        self.snake.head[1] += self.snake.movement[1]
        try:
            self.snake.body.pop(0)
        except IndexError:
            pass
        self.snake.body.append(self.snake.head[:])

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""

        # fill the screen with color
        self.screen.fill(self.settings.bg_color)

        # draw buttons and logo
        if not self.game_active:
            self.screen.blit(self.logo, (0, 50))
            if not self.settings_button_active:
                self.play_button.show_button()
                self.settings_button.show_button()
            else:
                # todo
                self.back_button.show_button()
                self.ai_button.show_button()
        else:   
            # draw fruit
            pygame.draw.rect(self.screen, self.fruit.color, (self.fruit.fruits[0], self.fruit.block))

            # draw snake
            #pygame.draw.rect(self.screen, self.snake.color, (self.snake.head, self.snake.block))
            for part in self.snake.body:
                pygame.draw.rect(self.screen, self.snake.color, (part, self.snake.block))

            # draw lines
            #self._lines()

        pygame.display.flip()
        sleep(0.1)

    def _check_collisions(self):
        """Handles collisions withe the fruit, snake body and borders"""
        if self.snake.head == self.fruit.fruits[0]:
            self.fruit.sound.play()
            self.fruit.fruits.pop()
            self.snake.grow()
        elif self.snake.head in self.snake.body[:-1]:
            self.game_active = False
            # todo: reset button and score
            self._reset_game()
        elif not 0-self.settings.block < self.snake.head[0] < self.settings.screen_size[0]\
        or not 0-self.settings.block < self.snake.head[1] < self.settings.screen_size[1]:
            self.game_active = False
            # todo: reset button and score
            self._reset_game()

    def run(self):
        """Main game loop"""
        while True:
            while not self.game_active:
                self._check_events()
                self._update_screen()
            while self.game_active:
                self._check_collisions()
                if not self.fruit.fruits:
                    self.fruit.new_fruit()
                self._check_events()
                if self.settings.ai_enabled:
                    self.ai.ai_move()
                self._update_snake()
                self._update_screen()


if __name__ == "__main__":
    sg = SnakeGame()
    sg.run()
