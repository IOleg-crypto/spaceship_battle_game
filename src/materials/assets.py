import os
import pygame as pg

""" Assets for game """

base_path = os.getcwd()
print(base_path)

programIcon = pg.image.load(os.path.join("assets/icon", "icon.png"))
spaceship = pg.image.load(os.path.join("assets/spaceships", "spaceship2d.png"))
shell_spaceship = pg.image.load(os.path.join("assets/shells", "shell.png"))
enemy_image_path = os.path.join("assets/spaceships", "spaceship2d_2.png")
alien_image_path = os.path.join("assets/invaders", "ufo.png")

# Background
loading_background = pg.image.load(os.path.join("assets/background", "space_background.png"))
