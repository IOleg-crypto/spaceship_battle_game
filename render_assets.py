import pygame as pg
from ammoability import AmmoAbility


class RenderSpaceShip:
    def __init__(self, pos, screen):
        self.pos = pos
        self.screen = screen

    def draw_ship(self, sprite_spaceship):
        scaled_image = pg.transform.scale(sprite_spaceship,
                                          (sprite_spaceship.get_width() // 4, sprite_spaceship.get_height() // 4))
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


class RenderSpaceShipShells(RenderSpaceShip):
    def __init__(self, pos, screen, sprite_shell, sprite_rocket):
        super().__init__(pos, screen)
        self.sprite_shell = sprite_shell
        self.sprite_rocket = sprite_rocket
        self.shells = []

    def draw_shell(self):
        scaled_image = pg.transform.scale(self.sprite_shell,
                                          (self.sprite_shell.get_width() // 4, self.sprite_rocket.get_height() // 4))
        rect = scaled_image.get_rect(center=(self.pos[0], self.pos[1]))  # Use self.pos to position the rect
        self.screen.blit(scaled_image, rect)  # Use the rect without additional position fix code

    def shoot_shell(self):
        shell_pos = self.pos[:]
        shell = AmmoAbility(shell_pos, self.sprite_shell, speed=10)
        self.shells.append(shell)
        print("shot shell")

    def update_shell(self):
        for shell in self.shells:
            shell.update()
            if shell.pos[1] < 0:
                self.shells.remove(shell)
                print(f"Number of bullets: {len(self.shells)}")

    def draw_bullets(self):
        for shell in self.shells:
            shell.draw(self.screen)

# TODO: add the following functions
