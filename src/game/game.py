import pygame as pg
import random
import os
import tkinter as tk
from tkinter import messagebox

from config import load_config
from utils import ResolutionException
from menu import MainMenu
from movement import handle_spaceship_movement
from entities import Enemy, RenderSpaceShip
from blast import Explosion, RenderSpaceShipShells
from utils import display_information, fps_counter, WHITE , RED


def create_enemies(screen, enemy_image_path, alien_image_path, num_enemies):
    images = [enemy_image_path, alien_image_path]
    enemies = [Enemy(screen, random.choice(images)) for _ in range(num_enemies)]
    return enemies


class Game:
    def __init__(self):
        self.shot_count = None
        self.score = None
        self.running = None
        self.enemy_shells = None
        self.config = load_config()
        self.sound_muted = self.config.getboolean("sound", "muted")
        self.game_over = True


        try:
            self.screen_width = self.config.getint("window", "width")
            self.screen_height = self.config.getint("window", "height")
            if self.screen_width < 640 or self.screen_height < 480:
                raise ResolutionException("Selected resolution is too small", 640, 480)
        except ResolutionException as e:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Resolution Error", str(e))
            raise SystemExit

        self.screen = pg.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pg.time.Clock()

        self.background = pg.image.load(
            os.path.join("assets", "background", "space_background.png")
        ).convert()

        self.spaceship_sprite = self.load_spaceship()
        self.shell_sprite = pg.image.load(os.path.join("assets", "shells", "shell.png")).convert_alpha()
        self.enemy_sprite_path = os.path.join("assets", "spaceships", "spaceship2d_2.png")
        self.alien_sprite_path = os.path.join("assets", "invaders", "ufo.png")

        self.icon = pg.image.load(os.path.join("assets", "icon", "icon.png")).convert_alpha()
        pg.display.set_icon(self.icon)
        pg.display.set_caption("Spaceship Battle!")

        self.spawn_enemies = 1 # By default

    def load_spaceship(self):
        default_path = os.path.join("assets", "spaceships", "spaceship2d.png")
        if self.config.has_option("player", "spaceship"):
            path = self.config.get("player", "spaceship")
            return pg.image.load(path).convert_alpha() if os.path.exists(path) else pg.image.load(default_path).convert_alpha()
        return pg.image.load(default_path).convert_alpha()

    def start_menu(self):
        menu = MainMenu(
            width=self.screen_width,
            height=self.screen_height,
            title="Spaceship Battle",
            screen=self.screen,
            start_game_callback=self.run_game_loop,
            enemies=self.spawn_enemies,
        )
        menu.draw_menu()

    def run_game_loop(self , enemies):
        self.running = True
        self.score = 0
        self.shot_count = 0
        self.spawn_enemies = enemies

        spaceship = RenderSpaceShip(
            [self.screen_width // 2, self.screen_height // 2],
            self.spaceship_sprite
        )

        all_sprites = pg.sprite.Group(spaceship)
        enemy_sprites = pg.sprite.Group()
        explosion_group = pg.sprite.Group()
        shells = RenderSpaceShipShells(self.shell_sprite)
        self.enemy_shells = pg.sprite.Group()

        enemies = create_enemies(self.screen, self.enemy_sprite_path, self.alien_sprite_path, enemies)
        for enemy in enemies:
            enemy_sprites.add(enemy)
            all_sprites.add(enemy)

        font = pg.font.Font("font/Pacifico.ttf", 32)

        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.display.flip()
                    running_program = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_1:
                        main_menu = MainMenu(
                            width=self.screen.get_width(),
                            height=self.screen.get_height(),
                            title="Spaceship Battle",
                            screen=self.screen,
                            start_game_callback=self.set_enemies_and_run,
                            # Making crash with multithreading - given argument without len
                            enemies=self.spawn_enemies
                        )
                        main_menu.draw_menu()

            keys = pg.key.get_pressed()
            if self.game_over:
                handle_spaceship_movement(keys, spaceship)

            if keys[pg.K_SPACE]:
                shells.shoot_shell(spaceship.rect.center)
                if not pg.mixer.get_busy() and not self.sound_muted:
                    shoot_sound = pg.mixer.Sound("sound/spaceship/spaceship_shoot.mp3")
                    shoot_sound.play()
                self.shot_count += 1

            for enemy in enemy_sprites:
                bullet = enemy.shoot()
                if bullet:
                    self.enemy_shells.add(bullet)
                    all_sprites.add(bullet)

            self.check_collisions_enemy(shells, enemy_sprites, all_sprites, explosion_group)

            all_sprites.update()
            shells.update()
            self.enemy_shells.update()
            explosion_group.update()

            self.screen.blit(self.background, (0, 0))
            display_information(font, self.shot_count, self.score, spaceship, self.screen)

            all_sprites.draw(self.screen)
            shells.draw(self.screen)
            self.enemy_shells.draw(self.screen)
            explosion_group.draw(self.screen)

            self.check_end_game(enemy_sprites, font, spaceship, keys , explosion_group , all_sprites)

            if keys[pg.K_2]:
                fps_counter(screen=self.screen, clock=self.clock)

            pg.display.flip()
            self.clock.tick(60)

        pg.quit()

    def check_collisions_enemy(self, shells, enemy_sprites, all_sprites, explosion_group):
        hits = pg.sprite.groupcollide(shells, enemy_sprites, True, True)
        for _, enemies_hit in hits.items():
            for enemy in enemies_hit:
                explosion = enemy.destroy()
                if explosion:
                    explosion_group.add(explosion)
                    all_sprites.add(explosion)
                self.score += 1

        collisions = pg.sprite.groupcollide(shells, self.enemy_shells, True, True)
        for sprite, shells_hit in collisions.items():
            for bullet in shells_hit:
                explosion = Explosion(bullet.rect.centerx, bullet.rect.centery)
                explosion_group.add(explosion)
                all_sprites.add(explosion)

    def check_end_game(self, enemy_sprites, font, spaceship, keys , explosion_group , all_sprites):
        if len(enemy_sprites) == 0:
            if not self.sound_muted:
                pg.mixer.Sound("sound/victory/victory.mp3").play()

            text = font.render("You won! Press 1 to exit", True, WHITE)
            rect = text.get_rect(center=self.screen.get_rect().center)
            self.screen.blit(text, rect)
            pg.display.flip()

            for bullet in self.enemy_shells:
                explosion = Explosion(bullet.rect.centerx, bullet.rect.centery)
                self.enemy_shells.remove(bullet)

            if keys[pg.K_1]:
                self.running = False
            return


        for bullet in self.enemy_shells:
            if pg.sprite.collide_rect(bullet, spaceship):
                if spaceship.take_damage(3) <= 0:
                    game_over_text = pg.font.Font("font/Pacifico.ttf", 36).render(
                        "Game Over! Press 1 to exit", True, RED
                    )
                    explosion = Explosion(spaceship.rect.centerx, spaceship.rect.centery)
                    explosion_group.add(explosion)
                    all_sprites.add(explosion)

                    rect = game_over_text.get_rect(center=self.screen.get_rect().center)
                    self.screen.blit(game_over_text, rect)
                    self.game_over = False
                    pg.mixer.music.stop()

                    if keys[pg.K_1]:
                        self.running = False
                    break

                bullet.kill()

    def set_enemies_and_run(self, enemies):
        self.spawn_enemies = enemies
        self.run_game_loop(enemies)
