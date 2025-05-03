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

sound_muted = False
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


def start_console(sound_mute: bool, screen_width: int, screen_height: int, enemies: int):
    global console_open
    if console_open:
        return
    else:
        console_open = True  # Mark the console as open
        root = tk.Tk()  # Create a new tkinter window
        root.withdraw()  # to hide the root window
        Console(sound_mute, screen_width=screen_width,
                screen_height=screen_height,
                enemies=enemies)  # Pass the root and sound_muted value to the Console class
        root.mainloop()  # Start the tkinter main event loop


class MainMenu:
    def __init__(self, width, height, title, screen, start_game_callback, fullscreen: bool, enemies: int):
        self.title = title
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = "Normal"
        self.start_game_callback = start_game_callback
        self.fullscreen = fullscreen
        self.bg = MovingBackground(screen, os.path.join("assets/background", "background.jpg"), 2)

        self.enemies = enemies
        self.custom_theme = pm.themes.THEME_DARK.copy()
        self.custom_theme.background_color = pm.baseimage.BaseImage(
            image_path=os.path.join("assets/background", "background.jpg"),
            drawing_mode=pm.baseimage.IMAGE_MODE_FILL
        )

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
        print(f"Difficulty set to: {self.difficulty}")

    def draw_menu(self):
        """Draws the menu and listens for events, including 2 for console toggle."""
        pg.mixer.init()

        main_menu = pm.Menu(title=self.title,
                            width=self.width,
                            height=self.height,
                            theme=self.custom_theme)

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

        if not sound_muted:
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
                    if event.key == pg.K_2:
                        print("Pressed 2")
                        console_thread = threading.Thread(target=start_console,
                                                          args=(self.set_sound_status, self.width, self.height,
                                                                self.enemies,))
                        console_thread.daemon = True
                        console_thread.start()

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
        global sound_muted
        sound_muted = mute
        pg.mixer.music.set_volume(config.getboolean("sound", "muted") or sound_muted)
        return sound_muted

    def set_fullscreen(self, fullscreen, **kwargs):
        """Set the fullscreen state."""
        self.fullscreen = fullscreen
        if self.fullscreen:
            pg.display.set_mode((self.width, self.height), pg.FULLSCREEN)
        else:
            pg.display.set_mode((self.width, self.height))
        print(f"Fullscreen mode is now {'enabled' if self.fullscreen else 'disabled'}.")
