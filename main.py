import pygame as pg
import pygame_menu as pm
import os
import functionality as ra

white = (255, 255, 255)


class MainMenu:
    def __init__(self, width, height, title, screen):
        self.title = title
        self.width = width
        self.height = height
        self.screen = screen

    def draw_menu(self):
        main_menu = pm.Menu(title=self.title,
                            width=self.width,
                            height=self.height,
                            theme=pm.themes.THEME_GREEN)
        main_menu.add.button('Play', main())
        main_menu.add.button(title="Exit", action=pm.events.EXIT,
                             font_color=white, background_color=white)

        main_menu.mainloop(self.screen)

def main():
    """
    main functionality
    :return:
    """

    pg.init()
    """Pygame initialization"""
    width, height = 800, 600
    screen = pg.display.set_mode((width, height))
    clock = pg.time.Clock()
    pg.display.set_caption("Spaceship Battle!")

    running_program = True

    """Spaceship coordinates"""
    spaceship_pos = [screen.get_width() // 2, screen.get_height() // 2]

    if not pg.get_init():
        print("Not launched pygame")
    else:
        print("Launched pygame")

    """Main menu"""
    main_menu = ra.MainMenu(width, height, "Spaceship Battle", screen)
    main_menu.draw_menu()
    """count"""
    count = 0
    score = 00000

    """Loading sprites"""
    spaceship = pg.image.load(os.path.join("assets", "spaceship2d.png"))
    shell_spaceship = pg.image.load(os.path.join("assets", "shell.png"))

    """Render spaceship and its shells"""
    render = ra.RenderSpaceShip(spaceship_pos, screen)
    render_ammo = ra.RenderSpaceShipShells(spaceship_pos, screen, shell_spaceship)

    """bool checker"""
    show_debug_text = True

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
        if keys[pg.K_SPACE] or keys[pg.K_KP_ENTER]:
            render_ammo.shoot_shell()
            count += 1
            print("Space key pressed")
        if keys[pg.K_x]:
            show_debug_text = not show_debug_text
            print("Debug text")

        # Fill the screen with a color to wipe away anything from last frame
        screen.fill("black")

        """display text"""
        font = pg.font.Font("font/Pacifico.ttf", 36)
        text_surface = font.render("Shooted bullets : " + str(count), True, white)
        text_score = font.render("Score : " + str(score), True, white)

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

        # Render the spaceship
        render.draw_ship(spaceship)

        # Render the bullets
        render_ammo.update_shells()
        render_ammo.draw_bullets()

        # Update the screen
        pg.display.update()

        # Flip the display to put your work on screen
        pg.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
