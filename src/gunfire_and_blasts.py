import pygame as pg
import os

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)


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


class RenderSpaceShipShells(pg.sprite.Group):
    def __init__(self, sprite_shell):
        super().__init__()
        self.sprite_shell = sprite_shell

    def shoot_shell(self, pos):
        shell = AmmoAbility(pos, self.sprite_shell, speed=5)
        self.add(shell)


class Explosion(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.image = []
        self.images = []
        for num in range(1, 8):  # loop to load next png(like animation)
            img = (pg.image.load(os.path.join("assets/explosions/explosion1", f"explosion{num}.png")))
            img = pg.transform.scale(img, (150, 150))
            self.images.append(img)
        self.frame_index = 0
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0

    def update(self):
        explosion_speed = 2
        self.counter += 1

        if self.counter >= explosion_speed and self.frame_index < len(self.images) - 1:
            self.frame_index += 2
            self.image = self.images[self.frame_index]

        if self.frame_index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()


class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y, speed_y, owner):
        super().__init__()
        self.image = pg.Surface((5, 10))
        self.image.fill((255, 0, 0))  # Red color for the bullet
        self.rect = self.image.get_rect(center=(x, y))
        self.speed_y = speed_y
        self.owner = owner

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0 or self.rect.top + 100 > pg.display.get_surface().get_height():
            self.kill()

    def check_collision(self, target_group):
        hits = pg.sprite.spritecollide(self, target_group, False)
        for hit in hits:
            if hit != self.owner:
                explosion = hit.take_damage(5)  # Reduce health by 10
                self.kill()
                if explosion:
                    return explosion
        return None
