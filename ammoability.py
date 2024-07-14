import pygame as pg
import os


class AmmoAbility:
    def __init__(self, pos, image, speed):
        self.pos = pos[:]
        self.image = image
        self.speed = speed
        self.rect = self.image.get_rect(center=self.pos)

    def update(self):
        self.pos[1] -= self.speed
        self.rect.center = self.pos

    def draw(self, screen):
        screen.blit(self.image, self.rect)
