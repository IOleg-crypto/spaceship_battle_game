import pygame as pg
import os
import pygame_menu as pm
import functionality as ra
import random

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

num_enemies = 14


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

    render = ra.RenderSpaceShip(spaceship_pos, spaceship)
    load_enemy = ra.Enemy(screen, enemy_image_path)

    all_sprites = pg.sprite.Group(render)
    enemy_sprite = pg.sprite.Group(load_enemy)
    shells = ra.RenderSpaceShipShells(shell_spaceship)

    main_menu = ra.MainMenu(width, height, "Spaceship Battle", screen,
                            lambda: game_loop(screen, clock, render, all_sprites, shells, load_enemy, enemy_sprite))
    main_menu.draw_menu()

def game_loop(screen, clock, render, all_sprites, shells, load_enemy, enemy_sprite):
    running_program = True
    count = 0
    score = 0

    loading_background = pg.image.load(os.path.join("assets/background", "space_background.png"))
    show_debug_text = True
    game_won = False

    while running_program:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running_program = False

        keys = pg.key.get_pressed()
        if not game_won:
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

        if pg.sprite.groupcollide(shells, enemy_sprite, True, True):
            score += 1

        pg.display.update()
        clock.tick(60)

    pg.quit()

if __name__ == "__main__":
    main()