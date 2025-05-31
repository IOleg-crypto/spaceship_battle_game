"""main.py - main game functionality"""

from pygame.locals import *

"""Structure of game"""
import configparser as cfg

from blast import RenderSpaceShipShells, Explosion
from entities import Enemy
from entities import RenderSpaceShip
from materials import *
from menu import MainMenu

"""For exception"""
import tkinter as tk
from tkinter import messagebox

from ResolutionException import ResolutionException

import random

global sound_muted
global console_open

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

"""Config read"""

config = cfg.ConfigParser()


def create_enemies(screen, enemy_image_path, alien_image_path, num_enemies):
    images = [enemy_image_path, alien_image_path]
    enemies = [Enemy(screen, random.choice(images)) for _ in range(num_enemies)]
    return enemies


def set_difficulty(num_enemies: int, screen) -> int:
    if MainMenu.get_difficulty == "Easy":
        num_enemies = 10
        if screen[0] > 800 or screen[1] > 600:
            num_enemies = 20
    elif MainMenu.get_difficulty == "Normal":
        num_enemies = 25
        if screen[0] > 800 or screen[1] > 600:
            num_enemies = 30
    else:
        num_enemies = 40
        if screen[0] > 800 or screen[1] > 600:
            num_enemies = 60
    return num_enemies



def display_information(font, count, score, render, screen):
    text_surface = font.render("Shot bullets : " + str(count), True, WHITE)
    text_score = font.render("Score : " + str(score), True, WHITE)
    text_health = font.render("Health : " + str(render.health), True, RED)

    text_rect = text_surface.get_rect()
    text_score_rect = text_score.get_rect()
    text_health_rect = text_health.get_rect()
    screen.blit(text_surface, text_rect)
    text_rect.topleft = (5, 10)
    text_score_rect.topleft = (text_rect.left, text_rect.bottom + 10)
    text_health_rect.topleft = (
        text_score_rect.left,
        text_score_rect.bottom + 10,
    )
    screen.blit(text_score, text_score_rect)
    screen.blit(text_health, text_health_rect)

def fps_counter(screen , clock):
    fps = str(int(clock.get_fps()))
    fps_text = font.render(f"FPS: {fps}", True, pg.Color("white"))
    screen.blit(fps_text, (10, 40))

def handle_spaceship_movement(keys, render):
    movement = {
        pg.K_LEFT: (-5, 0),
        pg.K_RIGHT: (5, 0),
        pg.K_UP: (0, -5),
        pg.K_DOWN: (0, 5),
        pg.K_w: (0, -5),
        pg.K_s: (0, 5),
        pg.K_a: (-5, 0),
        pg.K_d: (5, 0)
    }

    for key, (dx, dy) in movement.items():
        if keys[key]:
            render.update(dx, dy)


def main():
    config.read("config/config.cfg")
    fullscreen = config.getboolean("window", "fullscreen")
    sound_muted: bool = config.getboolean("sound", "muted")
    '''''''''''''''''''''''
        Screen Resolution
    '''''''''''''''''''''''
    try:
        screen_width = config.getint("window", "width")
        screen_height = config.getint("window", "height")
        if screen_width < 640 or screen_height < 480:
            raise ResolutionException("Selected resolution is too small", 640, 480)
    except ResolutionException as e:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Error", str(e))
        return -1

    # defined enemies to 0(not spawn)
    enemies = 0

    spawn_enemies = set_difficulty(enemies, screen=[screen_width, screen_height])

    pg.init()
    pg.mixer.init()
    flags = DOUBLEBUF
    screen = pg.display.set_mode((screen_width, screen_height), flags)
    clock = pg.time.Clock()
    pg.display.set_caption("Spaceship Battle!")

    pg.display.set_icon(programIcon)

    spaceship_pos = [screen.get_width() // 2, screen.get_height() // 2]

    spaceship_sprite = RenderSpaceShip(spaceship_pos, spaceship)
    load_enemy = Enemy(screen, enemy_sprite_path)
    all_sprites = pg.sprite.Group(spaceship_sprite)
    enemy_sprite = pg.sprite.Group(load_enemy)
    shells = RenderSpaceShipShells(shell_spaceship)

    explosion_group = pg.sprite.Group()

    # Create multiple enemies
    # Number of enemies to create
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
            spaceship,
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
