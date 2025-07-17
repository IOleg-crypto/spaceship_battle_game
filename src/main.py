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


def game_loop(screen, clock, render, all_sprites, shells, enemy_sprite, enemy_image_path: str, alien_image_path: str,
              num_enemies: int, explosion_group, count_enemies, spaceship, fullscreen, sound_muted: bool):
    """variable for game loop"""
    global font
    running_program = True
    game_finish = True
    count = 0
    score = 0
    render.health = 100

    Enemy(screen, random.choice([alien_image_path, enemy_image_path]))
    all_sprites = pg.sprite.Group(render)
    enemy_sprite = pg.sprite.Group()
    enemy_shells = pg.sprite.Group()
    spaceship_sprite = pg.sprite.Group()
    spaceship_sprite.add(render)

    count_enemies: list[Enemy] = create_enemies(screen, enemy_image_path, alien_image_path, num_enemies)
    """Spawn enemies"""
    for enemy in count_enemies:
        enemy_sprite.add(enemy)
        all_sprites.add(enemy)

    while running_program:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.display.flip()
                running_program = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_1:
                    main_menu = MainMenu(
                        width=screen.get_width(),
                        height=screen.get_height(),
                        title="Spaceship Battle",
                        screen=screen,
                        start_game_callback=lambda: main(),
                        # Making crash with multithreading - given argument without len
                        enemies=len(count_enemies)
                    )
                    main_menu.draw_menu()

        keys = pg.key.get_pressed()

        # Enemy shooting
        for enemy in enemy_sprite:
            bullet = enemy.shoot()
            if bullet:
                enemy_shells.add(bullet)
                all_sprites.add(bullet)

        for bullet in enemy_shells:
            if pg.sprite.spritecollideany(
                    render, enemy_shells
            ):  # Check collision with player's spaceship
                if render.take_damage(3) <= 0:  # Adjust damage as needed
                    game_finish = False
                    text_game_over = pg.font.Font("font/Pacifico.ttf", 36).render(
                        "Game Over! Press 1 to exit", True, RED
                    )
                    text_game_over_rect = text_game_over.get_rect()
                    text_game_over_rect.center = screen.get_rect().center
                    screen.blit(text_game_over, text_game_over_rect)
                    pg.mixer.music.stop()
                    if keys[pg.K_1]:
                        running_program = False
                        assert isinstance(fullscreen, object)
                        main_menu = MainMenu(
                            screen.get_width(),
                            screen.get_height(),
                            "Spaceship Battle",
                            screen,
                            lambda: game_loop(
                                screen,
                                clock,
                                render,
                                all_sprites,
                                shells,
                                enemy_sprite,
                                enemy_image_path,
                                alien_image_path,
                                num_enemies,
                                explosion_group,
                                count_enemies,
                                spaceship,
                                fullscreen=fullscreen
                            ),
                            fullscreen
                        )
                        main_menu.draw_menu()
                bullet.kill()  # Remove bullet after collision

        current_time = pg.time.get_ticks()
        keys = pg.key.get_pressed()
        if game_finish:
            handle_spaceship_movement(keys, render)
            if keys[pg.K_SPACE]:
                shells.shoot_shell(render.rect.center)
                if not pg.mixer.get_busy() or sound_muted:
                    shoot_sound = pg.mixer.Sound("sound/spaceship/spaceship_shoot.mp3")
                    shoot_sound.play()
                count += 1



        all_sprites.update()
        shells.update()
        enemy_sprite.update()
        spaceship_sprite.update()

        screen.blit(background, (0, 0))

        """display text"""
        font = pg.font.Font("font/Pacifico.ttf", 32)
        display_information(font, count, score, render, screen)

        all_sprites.draw(screen)
        enemy_sprite.draw(screen)

        shells.draw(screen)
        explosion_group.draw(screen)

        keys = pg.key.get_pressed()
        if keys[pg.K_2]:
           fps_counter(screen=screen ,clock=clock)


        # Handle enemy destruction and spaceship health reduction
        for enemy in enemy_sprite:
            if pg.sprite.groupcollide(
                    shells, enemy_sprite, True, True
            ):  # Replace with actual condition
                explosion = enemy.destroy()
                if explosion:  # Ensure explosion is not None
                    explosion_group.add(explosion)
                    all_sprites.add(explosion)
                score += 1

        collisions = pg.sprite.groupcollide(shells, enemy_shells, True, True)
        for sprite, shells_hit in collisions.items():
            for spaceship_shell in shells_hit:
                """Create explosion at correct coords"""
                explosion = Explosion(spaceship_shell.rect.x, spaceship_shell.rect.y)
                explosion_group.add(explosion)
                all_sprites.add(explosion)


        enemies_left = len(enemy_sprite)
        if enemies_left == 0:
            victory_sound = pg.mixer.Sound("sound/victory/victory.mp3")
            victory_sound.play()

        if enemies_left == 0:
            game_finish = False
            text_finish = font.render("You won! Press 1 to exit", True, WHITE)
            text_game_over = font.render(None, True, WHITE)  # to prevent over the text
            text_finish_rect = text_finish.get_rect()
            text_finish_rect.center = screen.get_rect().center
            screen.blit(text_finish, text_finish_rect)
            text_game_over_rect = text_game_over.get_rect()
            text_game_over_rect.center = screen.get_rect().center
            screen.blit(text_game_over, text_game_over_rect)
            "Disable damage after game over"
            for bullet in enemy_shells:
                explosion = Explosion(bullet.rect.centerx, bullet.rect.centery)
                explosion_group.add(explosion)
                all_sprites.add(explosion)
                bullet.kill()

            sound_muted = True
            if keys[pg.K_1]:
                running_program = False
                main_menu = MainMenu(
                    screen.get_width(),
                    screen.get_height(),
                    "Spaceship Battle",
                    screen,
                    lambda: main(),
                    fullscreen
                )
                main_menu.draw_menu()

        # Game over condition
        if render.health <= 0:
            text_game_over = font.render("Game Over! Press 1 to exit", True, RED)
            text_game_over_rect = text_game_over.get_rect()
            text_game_over_rect.center = screen.get_rect().center
            screen.blit(text_game_over, text_game_over_rect)
            pg.mixer.music.stop()
            if keys[pg.K_1]:
                running_program = False
                main_menu = MainMenu(
                    sound_muted,
                    screen.get_width(),
                    screen.get_height(),
                    "Spaceship Battle",
                    screen,
                    lambda: main(),
                    fullscreen
                )
                main_menu.draw_menu()



        explosion_group.update()
        pg.display.flip()
        clock.tick(60)

    pg.quit()


"""Start game , default shit"""
if __name__ == "__main__":
    main()
