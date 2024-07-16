import pygame as pg
import pygame_menu as pm
import os

RED = (255, 0, 0)
WHITE = (255, 255, 255)


class AmmoAbility:
    def __init__(self, pos, sprite, speed):
        self.pos = pos
        self.sprite = sprite
        self.speed = speed

    def update(self):
        self.pos[1] -= self.speed

    def draw(self, screen):
        scaled_image = pg.transform.scale(self.sprite, (self.sprite.get_width() // 4, self.sprite.get_height() // 4))
        rect = scaled_image.get_rect(center=(self.pos[0], self.pos[1]))
        screen.blit(scaled_image, rect)


class RenderSpaceShip:
    def __init__(self, pos, screen):
        self.pos = pos
        self.screen = screen

    def draw_ship(self, sprite_spaceship):
        scaled_image = pg.transform.scale(sprite_spaceship,
                                          (sprite_spaceship.get_width() // 4, sprite_spaceship.get_height() // 4))
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
        shell = AmmoAbility(shell_pos, self.sprite_shell, speed=10)
        self.shells.append(shell)
        print("Shot shell")

    def update_shells(self):
        for shell in self.shells:
            shell.update()
            if shell.pos[1] < 0:
                self.shells.remove(shell)
                print(f"Number of bullets: {len(self.shells)}")

    def draw_bullets(self):
        for shell in self.shells:
            shell.draw(self.screen)


class Enemy:
    def __init__(self):
        pass


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
        #print(f"Background image loaded: {os.path.exists(os.path.join('assets', 'background.jpg'))}")

        self.custom_theme = pm.themes.THEME_DARK.copy()
        self.custom_theme.background_color = pm.baseimage.BaseImage(
            image_path=os.path.join("assets", "background.jpg"),
            drawing_mode=pm.baseimage.IMAGE_MODE_FILL
        )
    def draw_background(self):
        self.bg.update()
        self.bg.draw()


    def draw_menu(self):
        main_menu = pm.Menu(title=self.title,
                            width=self.width,
                            height=self.height,
                            theme=self.custom_theme)
        main_menu.add.button('Play', self.start_game)
        main_menu.add.button('Exit', pm.events.EXIT, font_color=WHITE, background_color=RED)

        main_menu.mainloop(self.screen, bgfun=self.draw_background)


    def start_game(self):
        self.screen.fill((0, 0, 0))
        pg.display.update()
        self.start_game_callback()
