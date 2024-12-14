import pygame as pg
import os

"""Loaded assets for the game by default"""
programIcon = pg.image.load(os.path.join("assets", "icon/icon.png"))
spaceship = pg.image.load(os.path.join("assets/spaceships", "spaceship2d.png"))
shell_spaceship = pg.image.load(os.path.join("assets/shells", "shell.png"))
enemy_image_path = os.path.join("assets/spaceships", "spaceship2d_2.png")
alien_image_path = os.path.join("assets/invaders", "ufo.png")
enemy_image_path = os.path.join("assets/spaceships", "spaceship2d_2.png")

"background"
loading_background = pg.image.load(
        os.path.join("assets/background", "space_background.png")
)