import pygame as pg
import pygame_menu as pm
import random as rm
import os
import math

RED = (255, 0, 0)
WHITE = (255, 255, 255)


class Ammo:
    def __init__(self, pos, sprite, speed):
        self.pos = pos
        self.sprite = sprite
        self.speed = speed

    def update(self):
        self.pos[1] -= self.speed

    def draw(self, screen):
        scaled_image = pg.transform.scale(self.sprite,
                                          ((self.sprite.get_width() // 4), self.sprite.get_height() // 4))
        rect = scaled_image.get_rect(center=(self.pos[0], self.pos[1]))
        screen.blit(scaled_image, rect)


class RenderSpaceShip:
    def __init__(self, pos, screen):
        self.pos = pos
        self.screen = screen

    def draw_ship(self, sprite_spaceship):
        scaled_image = pg.transform.scale(sprite_spaceship,
                                          (
                                          (sprite_spaceship.get_width() // 4), int(sprite_spaceship.get_height() // 4)))
        rect = scaled_image.get_rect(center=(self.pos[0], self.pos[1]))
        self.screen.blit(scaled_image, rect)

    def move(self, x, y):
        self.pos[0] += x
        self.pos[1] += y
        self.detect_screen_bounds()

    def detect_screen_bounds(self):
        if self.pos[0] > self.screen.get_width():
            self.pos[0] = 0
        if self.pos[0] < 0:
            self.pos[0] = self.screen.get_width()
        if self.pos[1] > self.screen.get_height():
            self.pos[1] = 0
        if self.pos[1] < 0:
            self.pos[1] = self.screen.get_height()


class RenderSpaceShipShells(RenderSpaceShip):
    def __init__(self, pos, screen, sprite_shell):
        super().__init__(pos, screen)
        self.sprite_shell = sprite_shell
        self.shells = []

    def shoot_shell(self):
        shell_pos = self.pos[:]
        shell = Ammo(shell_pos, self.sprite_shell, speed=10)
        self.shells.append(shell)

    def update_shells(self):
        for shell in self.shells:
            shell.update()
            if shell.pos[1] < 0:
                self.shells.remove(shell)

    def draw_bullets(self):
        for shell in self.shells:
            shell.draw(self.screen)


class Enemy:
    def __init__(self, screen, color, radius, initial_pos=None):
        self.screen = screen
        self.color = color
        self.radius = radius
        self.speed = [rm.choice([-1, 1]), rm.choice([-1, 1])]  # Default speed (test)
        # Initialize position; if not provided, start from a random position
        if initial_pos is None:
            self.pos = [rm.randint(0, screen.get_width()), rm.randint(0, screen.get_height())]
        else:
            self.pos = list(initial_pos)  # Ensure it's a list

    def draw(self):
        pg.draw.circle(self.screen, self.color, (int(self.pos[0]), int(self.pos[1])), self.radius)

    def move(self):
        # Update position based on speed
        self.pos[0] += self.speed[0]
        self.pos[1] += self.speed[1]
        self.detect_screen_bounds()

    def detect_screen_bounds(self):
        if self.pos[0] > self.screen.get_width():
            self.pos[0] = 0
        elif self.pos[0] < 0:
            self.pos[0] = self.screen.get_width()
        if self.pos[1] > self.screen.get_height():
            self.pos[1] = 0
        elif self.pos[1] < 0:
            self.pos[1] = self.screen.get_height()



    def update(self):
        self.move()
        self.draw()


class MovingBackground:
    def __init__(self, screen, image_path, speed):
        self.screen = screen
        self.bg_image = pg.image.load(image_path)
        self.bg_image = pg.transform.scale(self.bg_image, (screen.get_width(), screen.get_height()))
        self.bg_y = 0
        self.speed = speed

    def update(self):
        self.bg_y += self.speed
        if self.bg_y >= self.screen.get_height():
            self.bg_y = 0

    def draw(self):
        self.screen.blit(self.bg_image, (0, self.bg_y))
        self.screen.blit(self.bg_image, (0, self.bg_y - self.screen.get_height()))


class MainMenu:
    def __init__(self, width, height, title, screen, start_game_callback):
        self.title = title
        self.width = width
        self.height = height
        self.screen = screen
        self.start_game_callback = start_game_callback
        # self.bg = MovingBackground(screen, os.path.join("assets", "background.jpg"), 2)
        # print(f"Background image loaded: {os.path.exists(os.path.join('assets', 'background.jpg'))}")
        """unused options"""
        self.resolution_options = [
            ('800x600', (800, 600)),
            ('1024x768', (1024, 768)),
            ('1280x720', (1280, 720)),
            ('1920x1080', (1920, 1080))
        ]
        self.custom_theme = pm.themes.THEME_DARK.copy()
        self.custom_theme.background_color = pm.baseimage.BaseImage(
            image_path=os.path.join("assets", "background.jpg"),
            drawing_mode=pm.baseimage.IMAGE_MODE_FILL
        )

        self.selected_resolution = (800, 600)

    def draw_menu(self):
        main_menu = pm.Menu(title=self.title,
                            width=self.width,
                            height=self.height,
                            theme=self.custom_theme)

        settings_menu = pm.Menu('Settings', self.width, self.height, theme=self.custom_theme)

        # settings_menu.add.selector('Resolution :', self.resolution_options, onchange=self.set_resolution)
        settings_menu.add.button('Back', pm.events.BACK)

        main_menu.add.button('Play', self.start_game)
        main_menu.add.button('Settings', settings_menu)
        main_menu.add.button('Exit', pm.events.EXIT, font_color=WHITE, background_color=RED)

        main_menu.mainloop(self.screen)

    def start_game(self) -> None:
        self.screen.fill((0, 0, 0))
        pg.display.update()
        self.start_game_callback()
