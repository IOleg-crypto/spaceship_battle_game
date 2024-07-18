import pygame as pg
import os
import pygame_menu as pm
import functionality as ra
import random

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)


def create_enemies(screen, color, radius, num_enemies):
    enemies = pg.sprite.Group()
    for _ in range(num_enemies):
        enemy = ra.Enemy(screen, color, radius)
        enemies.add(enemy)
    return enemies


num_enemies = 10


def main():
    pg.init()
    pg.mixer.init()
    width, height = 800, 600
    screen = pg.display.set_mode((width, height))
    clock = pg.time.Clock()
    pg.display.set_caption("Spaceship Battle!")

    enemies = create_enemies(screen, RED, 15, num_enemies)

    spaceship_pos = [screen.get_width() // 2, screen.get_height() // 2]
    spaceship = pg.image.load(os.path.join("assets", "spaceship2d.png"))
    shell_spaceship = pg.image.load(os.path.join("assets", "shell.png"))

    render = ra.RenderSpaceShip(spaceship_pos, spaceship)
    all_sprites = pg.sprite.Group(render)
    shells = ra.RenderSpaceShipShells(shell_spaceship)

    main_menu = ra.MainMenu(width, height, "Spaceship Battle", screen,
                            lambda: game_loop(screen, clock, render, all_sprites, shells, enemies))
    main_menu.draw_menu()


def game_loop(screen, clock, render, all_sprites, shells, enemies):
    running_program = True
    count = 0
    score = 0

    loading_background = pg.image.load(os.path.join("assets", "space_background.png"))
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
        enemies.update()

        screen.blit(loading_background, (0, 0))

        """display text"""
        font = pg.font.Font("font/Pacifico.ttf", 36)
        text_surface = font.render("Shooted bullets : " + str(count), True, WHITE)
        text_score = font.render("Score : " + str(score), True, WHITE)

        # Получение прямоугольника текста
        text_rect = text_surface.get_rect()
        text_score_rect = text_score.get_rect()
        # Отображение текста, если show_debug_text установлено в True
        if show_debug_text:
            screen.blit(text_surface, text_rect)
            # Set the position of the text
            text_rect.topleft = (10, 10)  # Example position, adjust as needed
            text_score_rect.topleft = (text_rect.left, text_rect.bottom + 10)  # Adjust the vertical gap as needed
            screen.blit(text_score, text_score_rect)
        else:
            screen.blit(text_score, text_score_rect)

        # Update the screen
        pg.display.update()

        all_sprites.draw(screen)
        shells.draw(screen)
        enemies.draw(screen)

        if pg.sprite.groupcollide(shells, enemies, True, True):
            score += 1

        if score == num_enemies:
            game_won = True
            show_debug_text = False
            text_finish = pg.font.Font("font/Pacifico.ttf", 36)
            text_finish_surface = text_finish.render("YOU WIN!Press 1 to exit", True, WHITE)
            text_finish_rect = text_finish_surface.get_rect()
            text_finish_rect.center = (screen.get_width() // 2, screen.get_height() // 2)
            screen.blit(text_finish_surface, text_finish_rect)

            keys = pg.key.get_pressed()
            if keys[pg.K_1]:

                running_program = False
                #text_score_rect = text_score.get_rect()
                text_score_rect.center = (screen.get_width() // 4, screen.get_height() // 4)
                main_menu = ra.MainMenu(screen.get_width(), screen.get_height(), "Spaceship Battle", screen,
                                        lambda: game_loop(screen, clock, render, all_sprites, shells, enemies))
                main_menu.draw_menu()

        pg.display.flip()
        clock.tick(60)

    pg.quit()


if __name__ == "__main__":
    main()
