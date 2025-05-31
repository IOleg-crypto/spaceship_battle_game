from blast import *

import pygame as pg

# Define color constants
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)


class RenderSpaceShip(pg.sprite.Sprite):
    def __init__(self, pos, sprite):
        super().__init__()
        self.image = pg.transform.scale(sprite, (sprite.get_width() // 8, sprite.get_height() // 8))
        self.rect = self.image.get_rect(center=pos)
        self.health = 100

    def update(self, x=0, y=0):
        self.rect.x += x
        self.rect.y += y
        self.detect_screen_bounds()

    def detect_screen_bounds(self):
        if self.rect.right > pg.display.get_surface().get_width()-2:
            self.rect.left = 0
        elif self.rect.left < 1:
            self.rect.right = pg.display.get_surface().get_width()
        if self.rect.bottom > pg.display.get_surface().get_height() - 2:
            self.rect.top = 0
        elif self.rect.top < 1:
            self.rect.bottom = pg.display.get_surface().get_height()

    def take_damage(self, amount):
        if amount == 0:
            return None
        self.health -= amount  # Correctly reduce health by the damage amount
        self.health = max(self.health, 0)  # Ensure health doesn't go below 0

        # Update health bar
        bar_length = self.image.get_width()
        bar_height = 7
        health_percentage = self.health / 100
        pg.draw.rect(self.image, RED, (0, 0, bar_length, bar_height))
        pg.draw.rect(self.image, GREEN, (0, 0, bar_length * health_percentage, bar_height))
        return self.health

    def destroy(self):
        explosion = Explosion(self.rect.centerx, self.rect.centery)
        return explosion
