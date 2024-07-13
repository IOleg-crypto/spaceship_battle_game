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
    spaceship_pos = [screen.get_width() // 2, screen.get_height() // 2, screen]
    if pg.get_init():
        print("Launched pygame")
    else:
        print("Not launched pygame")

        """Game loop"""
    """Loading sprites"""
    image_ship = pg.image.load(os.path.join("assets", "spaceship2d.png"))
    """Render spaceship and his shells"""
    render = ra.RenderSpaceShip(spaceship_pos, screen)
    while running_program:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window

        # event handling(set hotkeys and controls)
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


        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")

        # RENDER YOUR GAME HERE
        render.draw_ship(image_ship)

        # update the screen
        pg.display.update()

        # flip() the display to put your work on screen
        pg.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
