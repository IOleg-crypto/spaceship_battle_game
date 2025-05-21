"""Enemy realisation."""

import random
import pygame as pg

from blast import Explosion, Bullet


class Enemy(pg.sprite.Sprite):
    def __init__(self, screen: object, image_path: str):
        super().__init__()
        self.screen = screen
        self.image = pg.image.load(image_path)
        self.image = pg.transform.scale(self.image, (self.image.get_width() // 13, self.image.get_height() // 13))
        self.rect = self.image.get_rect(
            center=(int(random.randint(5, 350)), int(random.randint(6, 400))))
        self.speed = [3, 0]  # Move horizontally with a speed of 2
        self.shoot_delay = 3000  # milliseconds
        self.last_shot = pg.time.get_ticks()
        self.health = 200

    def update(self):
        if self.image:
            self.detect_screen_bounds()
            self.rect.x += self.speed[0]

    """
    Detect screen bounds to prevent problem(enemy ship spawn and don`t move. Cause he stuck!!!
    """

    def detect_screen_bounds(self):
        if self.rect.x + 20 >= self.screen.get_width() - self.rect.width - 1:
            self.speed[0] = -self.speed[0]

        if self.rect.x <= 0:
            self.speed[0] = -self.speed[0]
            """To prevent stuck"""
            self.rect.x = 2 # push enemy ship to the right

    def destroy(self):
        explosion = Explosion(self.rect.centerx, self.rect.centery)
        return explosion

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            explosion = Explosion(self.rect.centerx, self.rect.centery)
            self.kill()
            return explosion
        return None

    def shoot(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.bottom, 2, self)  # Speed 5 downwards
            return bullet
        return None
