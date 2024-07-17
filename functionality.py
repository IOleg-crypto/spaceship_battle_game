import pygame as pg
import pygame_menu as pm
import random
import os

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

class AmmoAbility(pg.sprite.Sprite):
    def __init__(self, pos, sprite, speed):
        super().__init__()
        self.image = pg.transform.scale(sprite, (sprite.get_width() // 4, sprite.get_height() // 4))
        self.rect = self.image.get_rect(center=pos)
        self.speed = speed

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

class RenderSpaceShip(pg.sprite.Sprite):
    def __init__(self, pos, sprite):
        super().__init__()
        self.image = pg.transform.scale(sprite, (sprite.get_width() // 4, sprite.get_height() // 4))
        self.rect = self.image.get_rect(center=pos)

    def update(self, x=0, y=0):
        self.rect.x += x
        self.rect.y += y
        self.detect_screen_bounds()

    def detect_screen_bounds(self):
        if self.rect.right > pg.display.get_surface().get_width():
            self.rect.left = 0
        elif self.rect.left < 0:
            self.rect.right = pg.display.get_surface().get_width()
        if self.rect.bottom > pg.display.get_surface().get_height():
            self.rect.top = 0
        elif self.rect.top < 0:
            self.rect.bottom = pg.display.get_surface().get_height()

class RenderSpaceShipShells(pg.sprite.Group):
    def __init__(self, sprite_shell):
        super().__init__()
        self.sprite_shell = sprite_shell

    def shoot_shell(self, pos):
        shell = AmmoAbility(pos, self.sprite_shell, speed=10)
        self.add(shell)

class Enemy(pg.sprite.Sprite):
    def __init__(self, screen, color, radius):
        super().__init__()
        self.screen = screen
        self.color = color
        self.radius = radius
        self.image = pg.Surface((radius * 2, radius * 2), pg.SRCALPHA)
        pg.draw.circle(self.image, color, (radius, radius), radius)
        self.rect = self.image.get_rect(center=(random.randint(0, screen.get_width()), random.randint(0, screen.get_height())))
        self.speed = [random.choice([-1, 1]), random.choice([-1, 1])]

    def update(self):
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]
        self.detect_screen_bounds()

    def detect_screen_bounds(self):
        if self.rect.right > self.screen.get_width():
            self.rect.left = 0
        elif self.rect.left < 0:
            self.rect.right = self.screen.get_width()
        if self.rect.bottom > self.screen.get_height():
            self.rect.top = 0
        elif self.rect.top < 0:
            self.rect.bottom = self.screen.get_height()

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
        self.bg = MovingBackground(screen, os.path.join("assets", "background.jpg"), 2)

        self.custom_theme = pm.themes.THEME_DARK.copy()
        self.custom_theme.background_color = pm.baseimage.BaseImage(
            image_path=os.path.join("assets", "background.jpg"),
            drawing_mode=pm.baseimage.IMAGE_MODE_FILL
        )

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

        while True:
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()

            self.bg.update()
            self.bg.draw()
            main_menu.update(events)
            main_menu.draw(self.screen)
            pg.display.flip()

    def start_game(self):
        self.screen.fill((0, 0, 0))
        pg.display.update()
        self.start_game_callback()
