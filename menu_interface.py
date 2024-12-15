import pygame_menu as pm
import configparser as cfgp
import level_design as ld
import tkinter as tk
from tkinter import filedialog
from assets import *

# Define color constants
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

sound_muted = False
config = cfgp.ConfigParser()
config.read("config/config.cfg")

def open_filedialog(file_path) -> str:
    # Initialize Tkinter and hide the root window
    root = tk.Tk()
    root.withdraw()

    # Open the file dialog
    file_path = filedialog.askopenfilename(
            title="Choose spaceship",
            filetypes=[("Image files(must be transparent)", "*.png")]
    )
    root.destroy()
    # Destroy the Tkinter instance
    return file_path




class MainMenu:
    def __init__(self, width, height, title, screen, start_game_callback , fullscreen : bool):
        self.title = title
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = "Normal"
        self.start_game_callback = start_game_callback
        self.fullscreen = fullscreen
        self.bg = ld.MovingBackground(screen, os.path.join("assets/background", "background.jpg"), 2)

        self.custom_theme = pm.themes.THEME_DARK.copy()
        self.custom_theme.background_color = pm.baseimage.BaseImage(
            image_path=os.path.join("assets/background", "background.jpg"),
            drawing_mode=pm.baseimage.IMAGE_MODE_FILL
        )

    def set_difficulty(self, value,  difficulty):
        self.difficulty = difficulty
        print(f"Difficulty set to: {self.difficulty}")

    def draw_menu(self):
        pg.mixer.init()

        sound_muted = config.getboolean("sound", "muted")

        if not sound_muted:
            # Load and play the music
            pg.mixer.music.load("sound/menu_music/stellar-discovery-219109.mp3")
            pg.mixer.music.play(-1)  # Play the music in a loop

        main_menu = pm.Menu(title=self.title,
                             width=self.width,
                             height=self.height,
                             theme=self.custom_theme)

        settings_menu = pm.Menu('Settings', self.width, self.height, theme=self.custom_theme)

        settings_menu.add.selector('Mute menu music :', [('Off', False), ('On', True)], onchange=self.set_sound_muted)
        settings_menu.add.selector(
            'Fullscreen: ',
            [('Off', False), ('On', True)],
            onchange=self.set_fullscreen
        )
        settings_menu.add.selector('Select difficulty:', [('Easy', 'Easy'), ('Normal', 'Normal'), ('Hard', 'Hard')],
                                   onchange=self.set_difficulty)
        settings_menu.add.button("Choose spaceship", lambda: open_filedialog(spaceship))


        settings_menu.add.button('Back', pm.events.BACK)


        # Add Play and Exit buttons to the main menu
        main_menu.add.button('Play', self.start_game)
        main_menu.add.button('Settings', settings_menu)
        main_menu.add.button('Exit', pm.events.EXIT, font_color=WHITE)

        # Run the main menu
        while True:
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()

            self.bg.update()
            self.bg.draw()

            main_menu.update(events)
            main_menu.draw(self.screen)
            pg.display.flip()

    def start_game(self):
        self.screen.fill((0, 0, 0))
        pg.display.update()
        self.start_game_callback()

    def set_sound_muted(self, value, mute):
        global sound_muted  # Declare sound_muted as global
        sound_muted = mute
        pg.mixer.music.set_volume(config.getboolean("sound", "muted") or sound_muted)

    def set_fullscreen(self, value, fullscreen, **kwargs):
        self.fullscreen = fullscreen
        if self.fullscreen:
            pg.display.set_mode((self.width, self.height), pg.FULLSCREEN)
        else:
            pg.display.set_mode((self.width, self.height))
        print(f"Fullscreen mode is now {'enabled' if self.fullscreen else 'disabled'}.")


