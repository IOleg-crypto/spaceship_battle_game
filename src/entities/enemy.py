"""Enemy realisation."""

import random
import pygame as pg

from blast import Explosion, Bullet


class Enemy(pg.sprite.Sprite):
    def __init__(self, screen: object, image_path: object) -> object:
        super().__init__()
        self.screen = screen
        self.image = pg.image.load(image_path)
        self.image = pg.transform.scale(self.image, (self.image.get_width() // 12, self.image.get_height() // 12))
        self.rect = self.image.get_rect(
            center=(int(random.randint(5, 400)), int(random.randint(6, 400))))
        self.speed = [3, 0]  # Move horizontally with a speed of 2
        self.shoot_delay = 3000  # milliseconds
        self.last_shot = pg.time.get_ticks()
        self.health = 200

    def update(self):
        if self.image:
            self.rect.x += self.speed[0]
            self.detect_screen_bounds()

    def detect_screen_bounds(self):
        if self.rect.x + 10 >= self.screen.get_width() - self.rect.width or self.rect.x <= 0:
            self.speed[0] = -self.speed[0]  # Reverse direction

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
