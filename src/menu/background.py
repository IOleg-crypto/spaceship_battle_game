import pygame as pg


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



