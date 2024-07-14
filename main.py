import pygame as pg
import os
import render_assets as ra


def main():
    """
    main functionality
    :return:
    """
    running_program = True

    """Pygame initialization"""
    pg.init()
    width, height = 800, 600
    screen = pg.display.set_mode((width, height))
    clock = pg.time.Clock()
    pg.display.set_caption("Spaceship Battle!")

    """Spaceship coordinates"""
    spaceship_pos = [screen.get_width() // 2, screen.get_height() // 2]
    if pg.get_init():
        print("Launched pygame")
    else:
        print("Not launched pygame")

    """Loading sprites"""
    spaceship = pg.image.load(os.path.join("assets", "spaceship2d.png"))
    shell_spaceship = pg.image.load(os.path.join("assets", "shell.png"))
    rocket_spaceship = pg.image.load(os.path.join("assets", "rocket.png"))

    """Render spaceship and its shells"""
    render = ra.RenderSpaceShip(spaceship_pos, screen)
    render_ammo = ra.RenderSpaceShipShells(spaceship_pos, screen, shell_spaceship, rocket_spaceship)

    """Game loop"""
    while running_program:
        # Event handling (set hotkeys and controls)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running_program = False

        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            render.move(-5, 0)
        if keys[pg.K_RIGHT]:
            render.move(5, 0)
        if keys[pg.K_UP]:
            render.move(0, -5)
        if keys[pg.K_DOWN]:
            render.move(0, 5)
        if keys[pg.K_w]:
            render.move(0, -5)
        if keys[pg.K_s]:
            render.move(0, 5)
        if keys[pg.K_a]:
            render.move(-5, 0)
        if keys[pg.K_d]:
            render.move(5, 0)
        if keys[pg.K_1]:
            render_ammo.draw_rocket()
        if keys[pg.K_SPACE]:
            render_ammo.draw_shell()

        # Fill the screen with a color to wipe away anything from last frame
        screen.fill("black")

        # Render the spaceship
        render.draw_ship(spaceship)

        # Update the screen
        pg.display.update()

        # Flip the display to put your work on screen
        pg.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
