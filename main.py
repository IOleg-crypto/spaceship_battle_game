import pygame as pg
import os
import functionality as ra
import random

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

num_enemies = 14


def create_enemies(screen, enemy_image_path, alien_image_path, num_enemies):
    enemies = [ra.Enemy(screen, random.choice([enemy_image_path, alien_image_path])) for _ in range(num_enemies)]
    return enemies


def main():
    pg.init()
    pg.mixer.init()
    width, height = 800, 600
    screen = pg.display.set_mode((width, height))
    clock = pg.time.Clock()
    pg.display.set_caption("Spaceship Battle!")
    programIcon = pg.image.load('assets/icon/icon.png')

    pg.display.set_icon(programIcon)

    spaceship_pos = [screen.get_width() // 2, screen.get_height() // 2]
    spaceship = pg.image.load(os.path.join("assets/spaceships", "spaceship2d.png"))
    shell_spaceship = pg.image.load(os.path.join("assets/shells", "shell.png"))
    enemy_image_path = os.path.join("assets/spaceships", "spaceship2d_2.png")
    alien_image_path = os.path.join("assets/invaders", "ufo.png")

    render = ra.RenderSpaceShip(spaceship_pos, spaceship)
    load_enemy = ra.Enemy(screen, enemy_image_path)
    all_sprites = pg.sprite.Group(render)
    enemy_sprite = pg.sprite.Group(load_enemy)
    shells = ra.RenderSpaceShipShells(shell_spaceship)

    explosion_group = pg.sprite.Group()

    # Create multiple enemies
    # Number of enemies to create
    enemies = [ra.Enemy(screen, random.choice([alien_image_path, enemy_image_path])) for _ in range(num_enemies)]
    for enemy in enemies:
        enemy_sprite.add(enemy)
        all_sprites.add(enemy)

    main_menu = ra.MainMenu(width, height, "Spaceship Battle", screen,
                            lambda: game_loop(screen, clock, render, all_sprites, shells, load_enemy, enemy_sprite,
                                              enemy_image_path, alien_image_path, num_enemies, explosion_group,
                                              enemies , spaceship))
    main_menu.draw_menu()


def game_loop(screen, clock, render, all_sprites, shells, main_menu, enemy_sprite, enemy_image_path, alien_image_path,
              num_enemies, explosion_group, enemies, spaceship):
    running_program = True
    game_finish = True
    show_debug_text = True
    count = 0
    score = 0

    enemy_image_path = os.path.join("assets/spaceships", "spaceship2d_2.png")
    load_enemy = ra.Enemy(screen, random.choice([alien_image_path, enemy_image_path]))
    loading_background = pg.image.load(os.path.join("assets/background", "space_background.png"))

    all_sprites = pg.sprite.Group(render)
    enemy_sprite = pg.sprite.Group()
    shells_enemy_sprite = pg.sprite.Group()
    bullet_group = pg.sprite.Group()
    spaceship_sprite = pg.sprite.Group()

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
                    main_menu = ra.MainMenu(
                        screen.get_width(), screen.get_height(), "Spaceship Battle", screen,
                        lambda: game_loop(screen, clock, render, all_sprites, shells, main_menu, enemy_sprite,
                                          enemy_image_path, alien_image_path,
                                          num_enemies, explosion_group, enemies , spaceship)
                    )
                    main_menu.draw_menu()

        # enemy shooting
        for enemy in enemy_sprite:
            bullet = enemy.shoot()
            if bullet:
                bullet_group.add(bullet)
                all_sprites.add(bullet)

        for bullet in shells_enemy_sprite:
            explosion = bullet.check_collision(enemy_sprite, bullet_group)
            if explosion:
                explosion_group.add(explosion)
                all_sprites.add(explosion)

        for bullet in bullet_group:
            if pg.sprite.spritecollide(bullet, spaceship_sprite, False):
                explosion = spaceship.take_damage(20)
                bullet.kill()
                if explosion:
                    explosion_group.add(explosion)
                    all_sprites.add(explosion)



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
                shells.shoot_shell(render.rect.center)
                if not ra.sound_muted:
                    # Play shooting sound
                    pg.mixer.Sound("sound/spaceship/spaceship_shoot.mp3").play(0, 0, 0)
                count += 1

        all_sprites.update()
        shells.update()
        enemy_sprite.update()
        spaceship_sprite.update(screen)



        screen.blit(loading_background, (0, 0))

        """display text"""
        font = pg.font.Font("font/Pacifico.ttf", 36)
        text_surface = font.render("Shooted bullets : " + str(count), True, WHITE)
        text_score = font.render("Score : " + str(score), True, WHITE)

        text_rect = text_surface.get_rect()
        text_score_rect = text_score.get_rect()
        if show_debug_text:
            screen.blit(text_surface, text_rect)
            text_rect.topleft = (10, 10)
            text_score_rect.topleft = (text_rect.left, text_rect.bottom + 10)
            screen.blit(text_score, text_score_rect)
        else:
            screen.blit(text_score, text_score_rect)

        all_sprites.draw(screen)
        enemy_sprite.draw(screen)
        shells.draw(screen)
        explosion_group.draw(screen)

        # Example condition to destroy an enemy (to be replaced with actual game logic)
        for enemy in enemy_sprite:
            if pg.sprite.groupcollide(shells, enemy_sprite, True, True):  # Replace with actual condition
                explosion = enemy.destroy()
                explosion_group.add(explosion)
                all_sprites.add(explosion)
                score += 1

        # Game over condition (fixed bug , that you can`t finish game , even enemies are destroyed)
        if len(enemy_sprite) == 0:
            game_finish = False
            text_finish = font.render("You won!Press 1 to exit", True, WHITE)
            text_finish_rect = text_finish.get_rect()
            text_finish_rect.center = screen.get_rect().center
            screen.blit(text_finish, text_finish_rect)

            pg.mixer.music.stop()
            pg.mixer.Sound("sound/victory/victory.mp3").play(0, 0, 0)
            if keys[pg.K_1]:
                running_program = False
                main_menu = ra.MainMenu(screen.get_width(), screen.get_height(), "Spaceship Battle", screen,
                                        lambda: game_loop(screen, clock, render, all_sprites, shells, load_enemy,
                                                          enemy_sprite, enemy_image_path, alien_image_path,
                                                          num_enemies, enemies, num_enemies))
                main_menu.draw_menu()


        pg.display.update()
        explosion_group.update()
        pg.display.flip()
        clock.tick(60)

    pg.quit()


if __name__ == "__main__":
    sound_muted = False  # Set this based on user settings
    main()
