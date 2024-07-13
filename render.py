import pygame as pg


class RenderSpaceShip:
    def __init__(self, pos, screen):
        self.pos = pos
        self.screen = screen

    def draw_ship(self, image):
        scaled_image = pg.transform.scale(image, (image.get_width() // 2, image.get_height() // 2 ))
        rect = scaled_image.get_rect()
        self.screen.blit(scaled_image, self.pos, rect)

    def move(self, x, y):
        self.pos[0] += x
        self.pos[1] += y

    def detect_screen_bounds(self):
        if self.pos[0] > 800:
            self.pos[0] = 0
        if self.pos[0] < 0:
            self.pos[0] = 800
        if self.pos[1] > 600:
            self.pos[1] = 0
        if self.pos[1] < 0:
            self.pos[1] = 600
