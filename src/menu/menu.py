import pygame_menu as pm
import configparser as cfg
import threading
import tkinter as tk
from tkinter import filedialog

from .background import MovingBackground
from .console import Console

"""materials"""
from src.materials import *

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

config = cfg.ConfigParser()
config.read("config/config.cfg")

console_open = False


def open_filedialog(file_path: str) -> str:
    """Opens the file dialog for choosing an entity image."""
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Choose entities",
        filetypes=[("Image files(must be transparent)", "*.png")]
    )
    root.destroy()
    return file_path


def start_console(sound_muted: bool, screen_width: int, screen_height: int, enemies: int):
    root = tk.Tk()
    root.withdraw()

    def on_close():
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)

    Console(sound_muted, screen_width, screen_height, enemies)  # Передаємо shared_data
    root.mainloop()


class MainMenu:

    def __init__(self, sound_muted: bool, width, height, title, screen, start_game_callback, fullscreen: bool, enemies: int):
        self.title = title
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = "Normal"
        self.start_game_callback = start_game_callback
        self.fullscreen = fullscreen
        self.bg = MovingBackground(screen, os.path.join("assets/background", "background.jpg"), 2)
        """To fix console issue(sound cmd not change bool"""
        self.sound_muted = sound_muted
        self.enemies = enemies
        self.custom_theme = pm.themes.THEME_DARK.copy()
        self.custom_theme.background_color = pm.baseimage.BaseImage(
            image_path=os.path.join("assets/background", "background.jpg"),
            drawing_mode=pm.baseimage.IMAGE_MODE_FILL
        )

    def set_difficulty(self, _label: str, difficulty: str):
        self.difficulty = difficulty
        if self.difficulty == "Easy":
            self.enemies = 10
        elif self.difficulty == "Normal":
            self.enemies = 25
        else:
            self.enemies = 40
        print(f"Difficulty set to: {self.difficulty}")

    def draw_menu(self):
        """Draws the menu and listens for events, including 2 for console toggle."""
        pg.mixer.init()

        main_menu = pm.Menu(title=self.title,
                            width=self.width,
                            height=self.height,
                            theme=self.custom_theme)
        """
        # Navigation inside settings menu
        """
        settings_menu = pm.Menu('Settings', self.width, self.height, theme=self.custom_theme)

        settings_menu.add.selector('Mute menu music :', [('Off', False), ('On', True)], onchange=self.set_sound_status)
        settings_menu.add.selector(
            'Fullscreen: ',
            [('Off', False), ('On', True)],
            onchange=self.set_fullscreen
        )
        settings_menu.add.selector('Select difficulty:', [('Easy', 'Easy'), ('Normal', 'Normal'), ('Hard', 'Hard')],
                                   onchange=self.set_difficulty)

        settings_menu.add.button("Choose entities", lambda: open_filedialog(spaceship))

        settings_menu.add.button('Back', pm.events.BACK)

        # Add Play and Exit buttons to the main menu
        main_menu.add.button('Play', self.start_game)
        main_menu.add.button('Settings', settings_menu)
        main_menu.add.button('Exit', pm.events.EXIT, font_color=WHITE)

        if not self.sound_muted:
            # Load and play the music
            pg.mixer.music.load("sound/menu_music/stellar-discovery-219109.mp3")
            pg.mixer.music.play(0)  # Play the music in a loop

        # Main menu event loop
        while True:
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()
                if event.type == pg.KEYDOWN:
                    """Make a console when key 2 is pressed"""
                    if event.key == pg.K_2:
                        print("Pressed 2")
                        """Using thread to make window"""
                        t = threading.Thread(
                            target=start_console,
                            args=(self.sound_muted, self.width, self.height, self.enemies),
                            daemon=True
                        )
                        t.start()

            self.bg.update()
            self.bg.draw()

            main_menu.update(events)
            main_menu.draw(self.screen)
            pg.display.flip()

    def start_game(self):
        """Start the game and switch to the game loop."""
        self.screen.fill((0, 0, 0))
        pg.display.update()
        self.start_game_callback()

    @staticmethod
    def set_sound_status(value, mute) -> bool:
        """Set whether the sound is muted."""
        sound_muted = mute
        pg.mixer.music.set_volume(config.getboolean("sound", "muted") or sound_muted)
        return sound_muted

    def set_fullscreen(self, _label: str, fullscreen: bool) -> bool:
        self.fullscreen = fullscreen
        """Set whether the game is in fullscreen mode."""
        if not fullscreen:
            self.screen = pg.display.set_mode((self.width, self.height))
        else:
            self.screen = pg.display.set_mode((self.width, self.height), pg.FULLSCREEN)
        self.bg.screen = self.screen
        """Just debug information"""
        print(f"Fullscreen mode is now {'enabled' if self.fullscreen else 'disabled'}.")
        return self.fullscreen
