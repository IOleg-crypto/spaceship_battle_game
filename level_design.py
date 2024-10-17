import pygame as pg
import random
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
        if self.rect.right > pg.display.get_surface().get_width():
            self.rect.left = 0
        elif self.rect.left < 0:
            self.rect.right = pg.display.get_surface().get_width()
        if self.rect.bottom > pg.display.get_surface().get_height():
            self.rect.top = 0
        elif self.rect.top < 0:
            self.rect.bottom = pg.display.get_surface().get_height()

    def take_damage(self, amount):
        self.health -= amount  # Correctly reduce health by the damage amount
        self.health = max(self.health, 0)  # Ensure health doesn't go below 0

        # Update health bar
        bar_length = self.image.get_width()
        bar_height = 5
        health_percentage = self.health / 100
        pg.draw.rect(self.image, RED, (0, 0, bar_length, bar_height))
        pg.draw.rect(self.image, GREEN, (0, 0, bar_length * health_percentage, bar_height))
        return self.health

    def destroy(self):
        explosion = Explosion(self.rect.centerx, self.rect.centery)
        return explosion


class RenderSpaceShipShells(pg.sprite.Group):
    def __init__(self, sprite_shell):
        super().__init__()
        self.sprite_shell = sprite_shell

    def shoot_shell(self, pos):
        shell = AmmoAbility(pos, self.sprite_shell, speed=5)
        self.add(shell)


# This class creates enemies (refactoring)
class Enemy(pg.sprite.Sprite):
    def __init__(self, screen, image_path):
        super().__init__()
        self.screen = screen
        self.image = pg.image.load(image_path)
        self.image = pg.transform.scale(self.image, (self.image.get_width() // 10, self.image.get_height() // 10))
        self.rect = self.image.get_rect(
            center=(int(random.randint(5, 400)), int(random.randint(6, 400))))
        self.speed = [3, 0]  # Move horizontally with a speed of 2
        self.shoot_delay = 2000  # milliseconds
        self.last_shot = pg.time.get_ticks()
        self.health = 200

    def update(self):
        if self.image:
            self.rect.x += self.speed[0]
            self.detect_screen_bounds()

    def detect_screen_bounds(self):
        if self.rect.x >= self.screen.get_width() - self.rect.width or self.rect.x <= 0:
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


# TODO : moving background(image) I donna fix this(I want make background , where moving stars , maybe it easy , but i`m slightly lazy)
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
        if self.rect.bottom < 0 or self.rect.top > pg.display.get_surface().get_height():
            self.kill()

    def check_collision(self, target_group):
        hits = pg.sprite.spritecollide(self, target_group, False)
        for hit in hits:
            if hit != self.owner:
                explosion = hit.take_damage(10)  # Reduce health by 10
                self.kill()
                if explosion:
                    return explosion
        return None
