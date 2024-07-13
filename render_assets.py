import pygame as pg


class RenderSpaceShip:
    def __init__(self, pos, screen):
        self.pos = pos
        self.screen = screen

    def draw_ship(self, image):
        scaled_image = pg.transform.scale(image, (image.get_width() // 4, image.get_height() // 4))
        rect = scaled_image.get_rect(center=(self.pos[0], self.pos[1]))  # Use self.pos to position the rect
        self.screen.blit(scaled_image, rect)  # Use the rect without additional position

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


class RenderSpaceShipShells:
    def __init__(self):n
        pass

    def draw_bullets(self):
        pass
