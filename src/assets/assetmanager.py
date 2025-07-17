import pygame as pg
import os

def load_image(path):
    return pg.image.load(path).convert_alpha()

def load_assets(config):
    background = load_image("assets/background/space_background.png")

    if config.has_option("player", "spaceship"):
        spaceship_path = config.get("player", "spaceship")
    else:
        spaceship_path = "assets/spaceships/spaceship2d.png"

    spaceship = load_image(spaceship_path)
    shell = load_image("assets/shells/shell.png")
    icon = load_image("assets/icon/icon.png")

    enemy_path = "assets/spaceships/spaceship2d_2.png"
    alien_path = "assets/invaders/ufo.png"

    return {
        "background": background,
        "spaceship": spaceship,
        "shell": shell,
        "icon": icon,
        "enemy": enemy_path,
        "alien": alien_path
    }
