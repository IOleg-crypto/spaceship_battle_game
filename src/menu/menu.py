
import threading
import tkinter as tk
from tkinter import filedialog

import pygame_menu as pm
import configparser as cfg

from .background import MovingBackground
from .console import Console
from src.materials import *  # your game materials

# Define color constants (if needed)
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

CONFIG_PATH = "config/config.cfg"


def open_filedialog(file_path: str) -> str:
    """Open file dialog to select an entity image."""
    root = tk.Tk()
    root.withdraw()
    selected_path = filedialog.askopenfilename(
        title="Choose entities",
        filetypes=[("Image files (transparent PNG)", "*.png")]
    )
    root.destroy()
    return selected_path or file_path


def start_console(sound_muted: bool, screen_width: int, screen_height: int, enemies: int):
    """Launch the game console window in a separate thread."""
    root = tk.Tk()
    root.withdraw()

    def on_close():
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    Console(sound_muted, screen_width, screen_height, enemies)
    root.mainloop()


class MainMenu:
    """Main menu class with settings persistence."""

    def __init__(self,
                 width: int,
                 height: int,
                 title: str,
                 screen,
                 start_game_callback: object,
                 enemies: int):
        # Load existing configuration or use defaults
        config = cfg.ConfigParser()
        config.read(CONFIG_PATH)

        # Config sections: [window], [sound], [game]
        self.width = config.getint("window", "width", fallback=width)
        self.height = config.getint("window", "height", fallback=height)
        self.sound_muted = config.getboolean("sound", "muted", fallback=False)
        self.volume = config.getfloat("sound", "volume", fallback=0.5)
        self.fullscreen = config.getboolean("window", "fullscreen", fallback=False)
        self.difficulty = config.get("game", "difficulty", fallback="Normal")
        # Apply difficulty to set enemy count
        self.set_difficulty(None, self.difficulty)

        # Store parameters
        self.title = title
        self.screen = screen
        self.start_game_callback = start_game_callback
        self.enemies = enemies

        # Create moving background
        self.bg = MovingBackground(
            screen,
            os.path.join("assets/background", "background.jpg"),
            2
        )
        # Copy and customize dark theme
        self.custom_theme = pm.themes.THEME_DARK.copy()
        self.custom_theme.background_color = pm.baseimage.BaseImage(
            image_path=os.path.join("assets/background", "background.jpg"),
            drawing_mode=pm.baseimage.IMAGE_MODE_FILL
        )
        self.volume_slider = None

    def save_config(self):
        """Write current settings back to the configuration file."""
        config = cfg.ConfigParser()
        config.read(CONFIG_PATH)
        # Ensure required sections are present
        if not config.has_section("window"): config.add_section("window")
        if not config.has_section("sound"): config.add_section("sound")
        if not config.has_section("game"): config.add_section("game")

        config.set("window", "width", str(self.width))
        config.set("window", "height", str(self.height))
        config.set("window", "fullscreen", str(self.fullscreen))
        config.set("sound", "muted", str(self.sound_muted))
        config.set("sound", "volume", str(self.volume))
        config.set("game", "difficulty", self.difficulty)

        with open(CONFIG_PATH, "w") as cfgfile:
            config.write(cfgfile)

    def set_difficulty(self, _label: str, difficulty: str):
        """Update game difficulty and adjust enemy count."""
        self.difficulty = difficulty
        if difficulty == "Easy":
            self.enemies = 10
        elif difficulty == "Normal":
            self.enemies = 25
        else:
            self.enemies = 40
        print(f"Difficulty set to: {difficulty}")
        self.save_config()

    def draw_menu(self):
        """Draw the main and settings menus and handle events."""
        pg.mixer.init()

        main_menu = pm.Menu(title=self.title,
                            width=self.width,
                            height=self.height,
                            theme=self.custom_theme)
        settings_menu = pm.Menu('Settings', self.width, self.height, theme=self.custom_theme)

        # Sound mute/unmute selector
        settings_menu.add.selector(
            'Mute menu music:',
            [('Off', False), ('On', True)],
            onchange=self.set_sound_status
        )
        # Fullscreen toggle selector
        settings_menu.add.selector(
            'Fullscreen:',
            [('Off', False), ('On', True)],
            onchange=self.set_fullscreen
        )
        # Volume slider with interactivity controlled by mute
        self.volume_slider = settings_menu.add.range_slider(
            title="Volume",
            default=self.volume,
            range_values=(0.0, 1.0),
            increment=0.05,
            onchange=self.on_volume_change
        )
        self.volume_slider.readonly = self.sound_muted

        # Difficulty selector
        settings_menu.add.selector(
            'Select difficulty:',
            [('Easy', 'Easy'), ('Normal', 'Normal'), ('Hard', 'Hard')],
            onchange=self.set_difficulty
        )
        # Open file dialog for custom entity images
        settings_menu.add.button(
            "Choose entities",
            lambda: open_filedialog(spaceship)
        )
        # Back button to main menu
        settings_menu.add.button('Back', pm.events.BACK)

        # Main menu buttons
        main_menu.add.button('Play', self.start_game)
        main_menu.add.button('Settings', settings_menu)
        main_menu.add.button('Exit', pm.events.EXIT, font_color=WHITE)

        # Play background music if not muted
        if not self.sound_muted:
            pg.mixer.music.load("sound/menu_music/stellar-discovery-219109.mp3")
            pg.mixer.music.set_volume(self.volume)
            pg.mixer.music.play(-1)

        # Main event loop
        while True:
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()
                if event.type == pg.KEYDOWN and event.key == pg.K_2:
                    threading.Thread(
                        target=start_console,
                        args=(self.sound_muted, self.width, self.height, self.enemies),
                        daemon=True
                    ).start()

            self.bg.update()
            self.bg.draw()
            main_menu.update(events)
            main_menu.draw(self.screen)
            pg.display.flip()

    def start_game(self):
        """Start the game and handle music pause/unpause."""
        self.screen.fill(BLACK)
        pg.display.update()
        self.start_game_callback()
        if self.sound_muted:
            pg.mixer.music.pause()
        else:
            pg.mixer.music.unpause()

    def set_sound_status(self, _label, mute: bool) -> bool:
        """Toggle mute state, update music playback and slider lock."""
        self.sound_muted = mute
        if self.sound_muted:
            pg.mixer.music.pause()
        else:
            if not pg.mixer.music.get_busy():
                pg.mixer.music.load("sound/menu_music/stellar-discovery-219109.mp3")
                pg.mixer.music.play(-1)
            pg.mixer.music.set_volume(self.volume)
        if self.volume_slider:
            self.volume_slider.readonly = self.sound_muted
        self.save_config()
        return self.sound_muted

    def on_volume_change(self, value: float):
        """Change music volume via slider if not muted and save."""
        self.volume = value
        if not self.sound_muted:
            pg.mixer.music.set_volume(self.volume)
        self.save_config()

    def set_fullscreen(self, _label: str, fullscreen: bool) -> bool:
        """Toggle fullscreen mode and save setting."""
        self.fullscreen = fullscreen
        if fullscreen:
            self.screen = pg.display.set_mode((self.width, self.height), pg.FULLSCREEN)
        else:
            self.screen = pg.display.set_mode((self.width, self.height))
        self.bg.screen = self.screen
        print(f"Fullscreen mode is now {'enabled' if fullscreen else 'disabled'}.")
        self.save_config()
        return fullscreen
