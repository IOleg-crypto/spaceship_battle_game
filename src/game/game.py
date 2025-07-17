from blast import Explosion
from entities import Enemy
from utils.Helper import display_information, fps_counter
from movement.movement import handle_spaceship_movement
from menu import MainMenu
from main import create_enemies


import pygame as pg
import random

WHITE = (255, 255, 255)
RED = (255, 0, 0)

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