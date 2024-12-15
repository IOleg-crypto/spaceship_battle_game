"""main.py - main game functionality"""
import random

import level_design as ld
import configparser as cfgp
import console as cls
import menu_interface as interface
from assets import *

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

def create_enemies(screen, enemy_image_path, alien_image_path, num_enemies):
    images = [enemy_image_path, alien_image_path]
    enemies = [ld.Enemy(screen, random.choice(images)) for _ in range(num_enemies)]
    return enemies


def main():
    config = cfgp.ConfigParser()
    config.read("config/config.cfg")
    fullscreen = config.getboolean("window" , "fullscreen")
    '''''''''''''''''''''''
        Screen Resolution
    '''''''''''''''''''''''
    screen_width, screen_height = config.getint("window", "width"), config.getint("window", "height")
    # defined enemies to 0(not spawn)
    num_enemies = 0

    if interface.MainMenu.set_difficulty == "Hard":
        if screen_width < 800 and screen_height < 600:
            num_enemies = random.randint(6 , 16)
        elif screen_width > 800 and screen_height > 600:
            num_enemies = random.randint(7, 25)
        if fullscreen:
            num_enemies = random.randint(7, 30)

    elif interface.MainMenu.set_difficulty == "Normal":
        if screen_width < 800 and screen_height < 600:
            num_enemies = random.randint(6 , 12)
        elif screen_width > 800 and screen_height > 600:
            num_enemies = random.randint(7, 19)
        if fullscreen:
            num_enemies = random.randint(7, 30)
    else:
        if screen_width < 800 and screen_height < 600:
            num_enemies = random.randint(6, 10)
        elif screen_width > 800 and screen_height > 600:
            num_enemies = random.randint(7, 10)
        if fullscreen:
            num_enemies = random.randint(7, 10)

    pg.init()
    pg.mixer.init()

    screen = pg.display.set_mode((screen_width, screen_height))
    clock = pg.time.Clock()
    pg.display.set_caption("Spaceship Battle!")

    pg.display.set_icon(programIcon)

    spaceship_pos = [screen.get_width() // 2, screen.get_height() // 2]

    render = ld.RenderSpaceShip(spaceship_pos, spaceship)
    load_enemy = ld.Enemy(screen, enemy_image_path)
    all_sprites = pg.sprite.Group(render)
    enemy_sprite = pg.sprite.Group(load_enemy)
    shells = ld.RenderSpaceShipShells(shell_spaceship)

    explosion_group = pg.sprite.Group()

    # Create multiple enemies
    # Number of enemies to create
    enemies = [
        ld.Enemy(screen, random.choice([alien_image_path, enemy_image_path]))
        for _ in range(num_enemies)
    ]
    for enemy in enemies:
        enemy_sprite.add(enemy)
        all_sprites.add(enemy)

    main_menu = interface.MainMenu(
        screen_width,
        screen_height,
        "Spaceship Battle",
        screen,
        lambda: game_loop(
            screen,
            clock,
            render,
            all_sprites,
            shells,
            load_enemy,
            enemy_sprite,
            enemy_image_path,
            alien_image_path,
            num_enemies,
            explosion_group,
            enemies,
            spaceship,
            config,
            fullscreen
        ),
        fullscreen

    )
    main_menu.draw_menu()


def game_loop(
        screen,
        clock,
        render,
        all_sprites,
        shells,
        main_menu,
        enemy_sprite,
        enemy_image_path,
        alien_image_path,
        num_enemies,
        explosion_group,
        enemies, spaceship, config ,fullscreen
):
    key_delay = 1500  # fix spawn bullets spam
    running_program = True
    game_finish = True
    show_debug_text = True
    count = 0
    score = 0
    render.health = 100

    load_enemy = ld.Enemy(screen, random.choice([alien_image_path, enemy_image_path]))

    console = cls.Console(config.getint("console", "width"), config.getint("console", "height"))




    all_sprites = pg.sprite.Group(render)
    enemy_sprite = pg.sprite.Group()
    shells_enemy_sprite = pg.sprite.Group()
    bullet_group = pg.sprite.Group()
    enemy_shells = pg.sprite.Group()
    spaceship_sprite = pg.sprite.Group()
    spaceship_sprite.add(render)

    enemies = create_enemies(screen, enemy_image_path, alien_image_path, num_enemies)
    for enemy in enemies:
        enemy_sprite.add(enemy)
        all_sprites.add(enemy)

    while running_program:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.display.flip()
                running_program = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_1:
                    main_menu = interface.MainMenu(
                        screen.get_width(),
                        screen.get_height(),
                        "Spaceship Battle",
                        screen,
                        lambda: main(
                            screen,
                            clock,
                            render,
                            all_sprites,
                            shells,
                            main_menu,
                            enemy_sprite,
                            enemy_image_path,
                            alien_image_path,
                            num_enemies,
                            explosion_group,
                            enemies,
                            spaceship,
                            config,
                            fullscreen
                        ),
                        fullscreen
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
                    game_lose = True
                    text_game_over = pg.font.Font("font/Pacifico.ttf", 36).render(
                        "Game Over! Press 1 to exit", True, RED
                    )
                    text_game_over_rect = text_game_over.get_rect()
                    text_game_over_rect.center = screen.get_rect().center
                    screen.blit(text_game_over, text_game_over_rect)
                    pg.mixer.music.stop()
                    if keys[pg.K_1]:
                        running_program = False
                        main_menu = interface.MainMenu(
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
                                load_enemy,
                                enemy_sprite,
                                enemy_image_path,
                                alien_image_path,
                                num_enemies,
                                explosion_group,
                                enemies,
                                spaceship,
                            ),
                        )
                        main_menu.draw_menu()
                bullet.kill()  # Remove bullet after collision

        last_shot_time = 0
        current_time = pg.time.get_ticks()
        keys = pg.key.get_pressed()
        if game_finish:
            if keys[pg.K_LEFT]:
                render.update(-5, 0)
            if keys[pg.K_RIGHT]:
                render.update(5, 0)
            if keys[pg.K_UP]:
                render.update(0, -5)
            if keys[pg.K_DOWN]:
                render.update(0, 5)
            if keys[pg.K_w]:
                render.update(0, -5)
            if keys[pg.K_s]:
                render.update(0, 5)
            if keys[pg.K_a]:
                render.update(-5, 0)
            if keys[pg.K_d]:
                render.update(5, 0)
            if keys[pg.K_x]:
                show_debug_text = not show_debug_text
            if keys[pg.K_SPACE]:
                # Check if enough time has passed since the last shot
                if current_time - last_shot_time > key_delay:
                    last_shot_time = current_time  # Update last shot time
                shells.shoot_shell(render.rect.center)
                if not interface.sound_muted or not pg.mixer.get_busy():
                    pg.mixer.Sound("sound/spaceship/spaceship_shoot.mp3").play(0, 0, 0)
                count += 1
            if keys[pg.K_BACKQUOTE]:
                console.toggle()


        all_sprites.update()
        shells.update()
        enemy_sprite.update()
        spaceship_sprite.update()

        screen.blit(loading_background, (0, 0))

        """display text"""
        font = pg.font.Font("font/Pacifico.ttf", 36)
        text_surface = font.render("Shooted bullets : " + str(count), True, WHITE)
        text_score = font.render("Score : " + str(score), True, WHITE)
        text_health = font.render("Health : " + str(render.health), True, RED)

        text_rect = text_surface.get_rect()
        text_score_rect = text_score.get_rect()
        text_health_rect = text_health.get_rect()
        if show_debug_text:
            screen.blit(text_surface, text_rect)
            text_rect.topleft = (10, 10)
            text_score_rect.topleft = (text_rect.left, text_rect.bottom + 10)
            text_health_rect.topleft = (
                text_score_rect.left,
                text_score_rect.bottom + 10,
            )
            screen.blit(text_score, text_score_rect)
            screen.blit(text_health, text_health_rect)
        else:
            screen.blit(text_score, text_score_rect)
            screen.blit(text_health, text_health_rect)

        all_sprites.draw(screen)
        enemy_sprite.draw(screen)
        shells.draw(screen)
        explosion_group.draw(screen)

        if console.is_open:
            console.handle_event(event)

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

        if len(enemy_sprite) == 0:
            game_finish = False
            text_finish = font.render("You won! Press 1 to exit", True, WHITE)
            text_game_over = font.render("", True, WHITE)  # to prevent over the text
            text_finish_rect = text_finish.get_rect()
            text_finish_rect.center = screen.get_rect().center
            screen.blit(text_finish, text_finish_rect)
            text_game_over_rect = text_game_over.get_rect()
            text_game_over_rect.center = screen.get_rect().center
            screen.blit(text_game_over, text_game_over_rect)
            pg.mixer.music.stop()
            pg.mixer.Sound("sound/victory/victory.mp3").play(0, 5, 0)
            if keys[pg.K_1]:
                running_program = False
                main_menu = interface.MainMenu(
                    screen.get_width(),
                    screen.get_height(),
                    "Spaceship Battle",
                    screen,
                    lambda: main(
                        screen,
                        clock,
                        render,
                        all_sprites,
                        shells,
                        load_enemy,
                        enemy_sprite,
                        enemy_image_path,
                        alien_image_path,
                        num_enemies,
                        enemies,
                        num_enemies,
                    ),
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
                main_menu = interface.MainMenu(
                    screen.get_width(),
                    screen.get_height(),
                    "Spaceship Battle",
                    screen,
                    lambda: main(
                        screen,
                        clock,
                        render,
                        all_sprites,
                        shells,
                        load_enemy,
                        enemy_sprite,
                        enemy_image_path,
                        alien_image_path,
                        num_enemies,
                        explosion_group,
                        enemies,
                        spaceship,
                    ),
                )
                main_menu.draw_menu()

        console.draw(screen)
        pg.display.update()
        explosion_group.update()
        pg.display.flip()
        clock.tick(60)


    pg.quit()


if __name__ == "__main__":
    sound_muted = False # Set this based on user settings
    main()
