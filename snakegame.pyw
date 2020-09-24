from time import sleep
from sys import exit
import pygame

from settings import Settings
from snake import Snake
from fruit import Fruit
from ai import AI
from button import Button
from score import Score


class SnakeGame:
    """Overall class to manage game assets and behavior"""

    def __init__(self):
        """Initialize the game, and create game resources"""

        pygame.init()

        # settings
        self.settings = Settings()

        # clock
        self.clock = pygame.time.Clock()

        # graphics
        self.logo = pygame.image.load("images/logo.png")
        self.game_over_logo = pygame.image.load("images/gameover.png")
        self.pause_logo = pygame.image.load("images/pause.png")
        self.how_to_play = pygame.image.load("images/howtoplay.png")

        # actives
        self.game_active = False
        self.settings_button_active = False
        self.game_over = False
        self.pause_active = False
        self.how_to_play_active = False
        self.movement_flag = False

        # screen
        self.screen = pygame.display.set_mode(self.settings.screen_size)
        pygame.display.set_caption("Snake")

        # objects
        self.snake = Snake(self)
        self.fruit = Fruit(self)
        self.ai = AI(self)
        self.score = Score(self)

        # lines
        self.lines = [
            i * self.settings.block for i in range(
                self.screen.get_rect().right // self.settings.block
            )
        ]

        # buttons
        # main menu buttons
        self.play_button = Button(
            self, (0, 100, 0), "PLAY",
            [i-j for i, j in zip(self.screen.get_rect().center, (50, 20))], (100, 40), 36
        )
        self.settings_button = Button(
            self, (0, 0, 0), "SETTINGS",
            (self.play_button.pos[0]-25, self.play_button.pos[1] + 80), (150, 40), 36
        )
        self.how_to_play_button = Button(
            self, (0, 0, 0), "HOW TO PLAY",
            (self.settings_button.pos[0] - 25, self.settings_button.pos[1] + 80), (200, 40), 36
        )

        # settings menu buttons
        self.ai_button = Button(
            self, (200, 0, 0), "AI DISABLED",
            (80, self.play_button.pos[1]), (180, 40), 36
        )
        self.lines_button = Button(
            self, (200, 0, 0), "LINES OFF",
            (80, self.play_button.pos[1] + 80), (180, 40), 36
        )
        self.sound_button = Button(
            self, (0, 200, 0), "SOUND ON",
            (340, self.play_button.pos[1]), (180, 40), 36
        )
        self.dark_mode_button = Button(
            self, (0, 0, 0), "LIGHT MODE",
            (340, self.play_button.pos[1] + 80), (180, 40), 36
        )

        # special buttons
        self.back_button = Button(
            self, (0, 0, 0), "BACK",
            (self.play_button.pos[0], self.play_button.pos[1] + 200), (100, 40), 36
        )
        self.reset_button = Button(
            self, (0, 0, 0), "MENU",
            (self.play_button.pos[0], self.play_button.pos[1] + 80), (100, 40), 36
        )
        self.quit_button = Button(
            self, (200, 0, 0), "QUIT",
            (self.play_button.pos[0], self.how_to_play_button.pos[1] + 80), (100, 40), 36
        )
        self.resume_button = Button(
            self, (0, 100, 0), "RESUME",
            (self.play_button.pos[0] - 20, self.play_button.pos[1]), (140, 40), 36
        )

    def _reset_game(self):
        """Resets the game"""
        self.game_active = False
        self.settings_button_active = False
        self.game_over = False
        self.pause_active = False
        self.how_to_play_active = False
        self.movement_flag = False
        self.snake = Snake(self)
        self.fruit = Fruit(self)
        self.score = Score(self)
        self.ai = AI(self)
        if self.settings.dark_mode_enabled:
            self.snake.color = (200, 200, 200)
            self.fruit.color = (200, 0, 0)

    def _check_events(self):
        """Handles events"""
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self._check_key_presses(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._check_mouse_clicks(event)
            elif event.type == pygame.QUIT:
                exit()

    def _check_key_presses(self, event):
        """Decides what to do when a button is pressed"""
        if not self.pause_active and not self.movement_flag:
            if event.key == pygame.K_UP:
                self.snake.move("UP")
            elif event.key == pygame.K_DOWN:
                self.snake.move("DOWN")
            elif event.key == pygame.K_LEFT:
                self.snake.move("LEFT")
            elif event.key == pygame.K_RIGHT:
                self.snake.move("RIGHT")
            elif event.key == pygame.K_ESCAPE:
                if self.game_active:
                    self.pause_active = True
                else:
                    exit()
        elif event.key == pygame.K_ESCAPE:
            if self.game_active:
                self.pause_active = False

    def _check_mouse_clicks(self, event):
        """Handles mouse actions"""
        if event.button == 1:
            # game over screen
            if self.game_over or self.pause_active:
                # reset button
                if self.reset_button.rect.collidepoint(*event.pos):
                    self._reset_game()
                # resume button
                elif self.resume_button.rect.collidepoint(*event.pos):
                    self.pause_active = False
                    sleep(1)
                # quit button
                elif self.quit_button.rect.collidepoint(*event.pos):
                    exit()
            elif not self.game_active:
                # main menu buttons
                if not self.settings_button_active and not self.how_to_play_active:
                    # play button
                    if self.play_button.rect.collidepoint(*event.pos):
                        self.game_active = True
                    # settings button
                    elif self.settings_button.rect.collidepoint(*event.pos):
                        self.settings_button_active = True
                    # how to play button
                    elif self.how_to_play_button.rect.collidepoint(*event.pos):
                        self.how_to_play_active = True
                    # quit button
                    elif self.quit_button.rect.collidepoint(*event.pos):
                        exit()
                # setting screen buttons
                elif self.settings_button_active:
                    # back button
                    if self.back_button.rect.collidepoint(*event.pos):
                        self.settings_button_active = False
                    # ai button
                    elif self.ai_button.rect.collidepoint(*event.pos):
                        self._check_ai()
                    # lines button
                    elif self.lines_button.rect.collidepoint(*event.pos):
                        self._check_lines()
                    # sound button
                    elif self.sound_button.rect.collidepoint(*event.pos):
                        self._check_sound()
                    # dark mode button
                    elif self.dark_mode_button.rect.collidepoint(*event.pos):
                        self._dark_mode()
                elif self.how_to_play_active:
                    # back button
                    if self.back_button.rect.collidepoint(*event.pos):
                        self.how_to_play_active = False

    def _dark_mode(self):
        """Turns dark mode on and off"""
        # turn dark mode off
        if self.settings.dark_mode_enabled:
            self.dark_mode_button.color = (0, 0, 0)
            self.dark_mode_button.text = "LIGHT MODE"
            self.dark_mode_button.font_color = (255, 255, 255)
            self.settings.bg_color = (200, 200, 200)
            self.snake.color = (0, 200, 0)
            self.fruit.color = (255, 0, 0)
            self.settings.dark_mode_enabled = False
        # turn dark mode on
        elif not self.settings.dark_mode_enabled:
            self.dark_mode_button.color = (200, 200, 200)
            self.dark_mode_button.text = "DARK MODE"
            self.dark_mode_button.font_color = (0, 0, 0)
            self.settings.bg_color = (55, 55, 55)
            self.snake.color = (200, 200, 200)
            self.fruit.color = (200, 0, 0)
            self.settings.dark_mode_enabled = True

    def _draw_lines(self):
        """Draws dividing lines"""
        for line in self.lines:
            pygame.draw.line(
                self.screen, (0, 0, 0), (0, line), (self.settings.screen_size[0], line)
            )
            pygame.draw.line(
                self.screen, (0, 0, 0), (line, 0), (line, self.settings.screen_size[1])
            )

    def _check_lines(self):
        """Enables and disables dividing lines"""
        if self.settings.lines_enabled:
            self.lines_button.color = (200, 0, 0)
            self.lines_button.text = "LINES OFF"
            self.settings.lines_enabled = False
        elif not self.settings.lines_enabled:
            self.lines_button.color = (0, 200, 0)
            self.lines_button.text = "LINES ON"
            self.settings.lines_enabled = True

    def _check_sound(self):
        """Enables and disables sound"""
        if self.settings.sound_enabled:
            self.sound_button.color = (200, 0, 0)
            self.sound_button.text = "SOUND OFF"
            self.settings.sound_enabled = False
        elif not self.settings.sound_enabled:
            self.sound_button.color = (0, 200, 0)
            self.sound_button.text = "SOUND ON"
            self.settings.sound_enabled = True

    def _check_ai(self):
        """Enables and disables AI"""
        if self.settings.ai_enabled:
            self.ai_button.color = (200, 0, 0)
            self.ai_button.text = "AI DISABLED"
            self.settings.ai_enabled = False
        elif not self.settings.ai_enabled:
            self.ai_button.color = (0, 200, 0)
            self.ai_button.text = "AI ENABLED"
            self.settings.ai_enabled = True

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
        """Update images on the screen, and flip to the new screen"""

        # fill the screen with color
        self.screen.fill(self.settings.bg_color)

        # draw graphics and buttons
        # game over
        if self.game_over:
            self.screen.blit(self.game_over_logo, (0, 50))
            self.reset_button.show_button()
            self.quit_button.show_button()
            self.score.save_high_score()
            self.score.show_score()

        # game active
        elif self.game_active:
            # draw fruit
            pygame.draw.rect(
                self.screen, self.fruit.color, (self.fruit.fruits[0], self.fruit.block)
            )

            # draw snake
            for part in self.snake.body:
                pygame.draw.rect(self.screen, self.snake.color, (part, self.snake.block))

            # draw lines
            if self.settings.lines_enabled:
                self._draw_lines()

            # pause
            if self.pause_active:
                self.screen.blit(self.pause_logo, (0, 50))
                self.score.show_score(pause=True)
                self.resume_button.show_button()
                self.reset_button.show_button()
                self.quit_button.show_button()

        # menu
        elif not self.game_active:
            self.screen.blit(self.logo, (0, 50))
            # settings menu
            if self.settings_button_active:
                self.lines_button.show_button()
                self.back_button.show_button()
                self.ai_button.show_button()
                self.sound_button.show_button()
                self.dark_mode_button.show_button()
            # how to play screen
            elif self.how_to_play_active:
                self.screen.fill((255, 255, 255))
                self.screen.blit(self.how_to_play, (0, 0))
                self.back_button.show_button()
            # main menu
            else:
                self.play_button.show_button()
                self.settings_button.show_button()
                self.how_to_play_button.show_button()
                self.quit_button.show_button()

        pygame.display.flip()

        self.clock.tick(10)

    def _check_collisions(self):
        """Handles collisions with the fruit, snake body and borders"""
        if self.snake.head == self.fruit.fruits[0]:
            if self.settings.sound_enabled:
                self.fruit.sound.play()
            self.fruit.fruits.pop()
            self.snake.grow()
            self.score.score += 10
        elif self.snake.head in self.snake.body[:-1]:
            self.game_active = False
            self.game_over = True
        elif not 0-self.settings.block < self.snake.head[0] < self.settings.screen_size[0]\
        or not 0-self.settings.block < self.snake.head[1] < self.settings.screen_size[1]:
            self.game_active = False
            self.game_over = True

    def run(self):
        """Main game loop"""
        while True:
            while not self.game_active:
                pygame.mouse.set_visible(True)
                self._check_events()
                self._update_screen()
                pygame.mouse.set_visible(False)
            while self.game_active:
                while self.pause_active:
                    pygame.mouse.set_visible(True)
                    self._check_events()
                    self._update_screen()
                    pygame.mouse.set_visible(False)
                self._check_collisions()
                if not self.fruit.fruits:
                    self.fruit.new_fruit()
                self._check_events()
                self.movement_flag = False
                if self.settings.ai_enabled:
                    self.ai.ai_move()
                self._update_snake()
                self._update_screen()


if __name__ == "__main__":
    sg = SnakeGame()
    sg.run()
