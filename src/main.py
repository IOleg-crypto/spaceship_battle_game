"""main.py - main game functionality"""
import os

from pygame import DOUBLEBUF

"""Structure of game"""
import configparser as cfg

from blast import RenderSpaceShipShells, Explosion
from entities import Enemy
from entities import RenderSpaceShip
from menu import MainMenu , spaceship_path_new
import pygame as pg

"""For exception"""
import tkinter as tk
from tkinter import messagebox

from utils.ResolutionException import ResolutionException

import random


global console_open



WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
"""Just assets for game"""
background = None
spaceship_sprite = None
shell_sprite = None
enemy_sprite_path = None
alien_sprite_path = None
program_icon = None

"""Config read"""
config = cfg.ConfigParser()


"""Creating enemies by number"""
def create_enemies(screen, enemy_image_path, alien_image_path, num_enemies):
    images = [enemy_image_path, alien_image_path]
    enemies = [Enemy(screen, random.choice(images)) for _ in range(num_enemies)]
    return enemies




def main():
    config.read("config/config.cfg")
    sound_muted: bool = config.getboolean("sound", "muted")


    try:
        screen_width  = config.getint("window", "width")
        screen_height = config.getint("window", "height")
        if screen_width < 640 or screen_height < 480:
            raise ResolutionException("Selected resolution is too small", 640, 480)
    except ResolutionException as e:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Error", str(e))
        return -1

    enemies = 0
    spawn_enemies = set_difficulty(enemies, screen=[screen_width, screen_height])

    pg.init()
    pg.mixer.init()
    screen = pg.display.set_mode((screen_width, screen_height), flags)
    global background, spaceship_sprite, shell_sprite
    global enemy_sprite_path, alien_sprite_path, program_icon



    background = pg.image.load(
        os.path.join("assets", "background", "space_background.png")
    ).convert_alpha()

    if os.path.exists(spaceship_path_new):
        spaceship_path = spaceship_path_new
    elif config.has_option("player", "spaceship"):
        spaceship_path_config = config.get("player", "spaceship")
        if os.path.exists(spaceship_path_config):
            spaceship_path = spaceship_path_config
        else:
            spaceship_path = os.path.join("assets", "spaceships", "spaceship2d.png")
    else:
        spaceship_path = os.path.join("assets", "spaceships", "spaceship2d.png")

    spaceship_sprite = pg.image.load(spaceship_path).convert_alpha()

    shell_sprite = pg.image.load(
        os.path.join("assets", "shells", "shell.png")
    ).convert_alpha()

    # ← restore this line so program_icon is a real Surface:
    program_icon = pg.image.load(
        os.path.join("assets", "icon", "icon.png")
    ).convert_alpha()

    enemy_sprite_path = os.path.join("assets", "spaceships", "spaceship2d_2.png")
    alien_sprite_path = os.path.join("assets", "invaders", "ufo.png")
    # Set the window icon AFTER mat.program_icon has been loaded
    pg.display.set_icon(program_icon)
    pg.display.set_caption("Spaceship Battle!")
    clock = pg.time.Clock()
    # ──────────────────────────────────────────────────────────────────────────────

    spaceship_pos = [screen.get_width() // 2, screen.get_height() // 2]
    spaceship_sprite = RenderSpaceShip(spaceship_pos, spaceship_sprite)
    load_enemy = Enemy(screen, enemy_sprite_path)
    all_sprites   = pg.sprite.Group(spaceship_sprite)
    enemy_sprite  = pg.sprite.Group(load_enemy)
    shells        = RenderSpaceShipShells(shell_sprite)
    explosion_group = pg.sprite.Group()

    enemies = [
        Enemy(screen, random.choice([alien_sprite_path, enemy_sprite_path]))
        for _ in range(spawn_enemies)
    ]
    for enemy in enemies:
        enemy_sprite.add(enemy)
        all_sprites.add(enemy)

    main_menu = MainMenu(
        width=screen_width,
        height=screen_height,
        title="Spaceship Battle",
        screen=screen,
        start_game_callback=lambda: game_loop(
            screen,
            clock,
            spaceship_sprite,
            all_sprites,
            shells,
            enemy_sprite,
            enemy_sprite_path,
            alien_sprite_path,
            spawn_enemies,
            explosion_group,
            enemies,
            spaceship_sprite,
            config,
            sound_muted=sound_muted
        ),
        enemies=spawn_enemies,
    )

    main_menu.draw_menu()
    return None


"""Start game , default shit"""
if __name__ == "__main__":
    main()
