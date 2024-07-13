import pygame as pg


class RenderSpaceShip:
    def __init__(self, pos, screen):
        self.pos = pos
        self.screen = screen

    def draw_ship(self, screen):
        pg.draw.circle(screen, "red", self.pos, 20)

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
