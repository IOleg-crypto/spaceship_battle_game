from render_assets import RenderSpaceShip, RenderSpaceShipShells
import pygame as pg
import os


class AmmoAbility(RenderSpaceShipShells, RenderSpaceShip):
    def __init__(self, pos, screen, bullet_list):
        super().__init__(pos, screen)
        self.pos = pos
        self.screen = screen
        self.bullet_list = bullet_list

    def draw_abilities(self, sprite_abilities):
        scaled_image = pg.transform.scale(sprite_abilities,
                                          (sprite_abilities.get_width() // 4, sprite_abilities.get_height() // 4))
        rect = scaled_image.get_rect(center=(self.pos[0], self.pos[1]))  # Use self.pos to position the rect
        self.screen.blit(scaled_image, rect)  # Use the rect without additional position
