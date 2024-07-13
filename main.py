import pygame as pg
import os
import random as rm
import render as r


def main():
    """
    main functionality
    :return:
    """
    """Spaceship coordinates"""
    spaceship_pos = [rm.randint(0, 800), rm.randint(0, 600)]
    """Pygame initialization"""
    pg.init()
    width, height = 800, 600
    screen = pg.display.set_mode((width, height))
    clock = pg.time.Clock()
    pg.display.set_caption("Spaceship Battle!")

    if pg.get_init():
        print("Launched pygame")
    else:
        print("Not launched pygame")

    """Render spaceship"""
    render = r.RenderSpaceShip(spaceship_pos, screen)
    """Loading sprites"""
    image_ship = pg.image.load(os.path.join("assets", "spaceship2d.png"))
    """Game loop"""
    while True:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window

        # event handling(set hotkeys and controls)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()

        """Move spaceship"""
        if pg.key.get_pressed()[pg.K_LEFT]:
            render.move(-5, 0)
        if pg.key.get_pressed()[pg.K_RIGHT]:
            render.move(5, 0)
        if pg.key.get_pressed()[pg.K_UP]:
            render.move(0, -5)
        if pg.key.get_pressed()[pg.K_DOWN]:
            render.move(0, 5)


        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")

        # RENDER YOUR GAME HERE
        render.draw_ship(image_ship)
        # detect screen bounds
        render.detect_screen_bounds()

        # update the screen
        pg.display.update()

        # flip() the display to put your work on screen
        pg.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
