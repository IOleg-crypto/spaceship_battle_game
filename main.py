import pygame as pg
import sys
import random as rm

pg.init()
width, height = 800, 600
BLOCK_SIZE = 50
screen = pg.display.set_mode((width, height))
clock = pg.time.Clock()


def main():
    while True:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")

        # RENDER YOUR GAME HERE

        # flip() the display to put your work on screen
        pg.display.flip()

        clock.tick(60)


if __name__ == "__main__":
    main()
