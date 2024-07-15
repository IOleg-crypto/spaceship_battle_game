import pygame as pg
import pygame_menu as pm
from main import *

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 100, 100)
BLACK = (0, 0, 0)
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


# TODO : need to make enemies and main menu

class Enemy:
    def __init__(self):
        pass


