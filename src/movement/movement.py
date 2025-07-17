import pygame as pg

def handle_spaceship_movement(keys, render):
    movement = {
        pg.K_LEFT: (-5, 0),
        pg.K_RIGHT: (5, 0),
        pg.K_UP: (0, -5),
        pg.K_DOWN: (0, 5),
        pg.K_w: (0, -5),
        pg.K_s: (0, 5),
        pg.K_a: (-5, 0),
        pg.K_d: (5, 0)
    }

    for key, (dx, dy) in movement.items():
        if keys[key]:
            render.update(dx, dy)