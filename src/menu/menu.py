import configparser as cfg
import os
import threading
import tkinter as tk
from tkinter import filedialog

import pygame as pg
import pygame_menu as pm

from . import console as console_module  # to read/write console_module.default_sound_muted
from .background import MovingBackground
from .console import Console

# Color constants (if needed elsewhere)
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
config = cfg.ConfigParser()


def console_process(sound_muted: bool, width: int, height: int, enemies: int):
    """
    Launch the Console window in a separate thread.
    Parameters:
        sound_muted: initial mute state (True/False)
        width: main game window width
        height: main game window height
        enemies: number of enemies to spawn
    """
    root = tk.Tk()
    root.title("Console")
    root.iconify()

    def on_close():
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)

    # Create an instance of Console (tk.Toplevel)
    console = Console(
        sound_muted=sound_muted,
        screen_width=width,
        screen_height=height,
        enemies=enemies,
    )
    console.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()


def open_filedialog(file_path: str):
    """
    Open a file dialog to let the user select a PNG spaceship image.
    Returns the selected file path as a string.
    """
    root = tk.Tk()
    root.withdraw()
    selected_path = filedialog.askopenfilename(
        title="Choose spaceship",
        filetypes=[("Image files (transparent PNG)", "*.png")]
    )
    root.destroy()
    print(selected_path)
    return selected_path


class MainMenu:
    """Main menu class that handles settings persistence and menu drawing."""

    spaceship_path = None
    status_music = None
    fullscreen_status = None
    createdConsole = 0

    def __init__(
        self,
        width: int,
        height: int,
        title: str,
        screen,
        start_game_callback: object,
        enemies: int
    ):
        # Load existing configuration or use defaults
        config.read(CONFIG_PATH)

        # Retrieve window dimensions and fullscreen flag
        self.width = config.getint("window", "width", fallback=width)
        self.height = config.getint("window", "height", fallback=height)
        self.sound_muted = config.getboolean("sound", "muted", fallback=False)
        self.volume = config.getfloat("sound", "volume", fallback=0.5)
        self.fullscreen = config.getboolean("window", "fullscreen", fallback=False)
        self.difficulty = config.get("game", "difficulty", fallback="Normal")

        # Set enemy count based on difficulty
        self.set_difficulty(None, self.difficulty)

        # Counter for how many times "Play" was clicked, so settings are preserved
        self.check_play_game = 0
        self.spaceship_path = None
        self.status_music = None
        self.fullscreen_status = None
        self.createdConsole = 0
        self.console_process = None

        # Store title, screen, callback, and initial enemy count
        self.title = title
        self.screen = screen
        self.start_game_callback = start_game_callback
        self.enemies = enemies

        # Initialize the moving background for the menu
        self.bg = MovingBackground(
            screen,
            os.path.join("assets/background", "background.jpg"),
            2
        )
        # Copy and customize the dark theme for pygame_menu
        self.custom_theme = pm.themes.THEME_DARK.copy()
        self.custom_theme.background_color = pm.baseimage.BaseImage(
            image_path=os.path.join("assets/background", "background.jpg"),
            drawing_mode=pm.baseimage.IMAGE_MODE_FILL
        )
        self.volume_slider = None

    def save_config(self):
        """
        Write the current settings back to the configuration file.
        Ensures that the [window], [sound], and [game] sections exist.
        """
        config.read(CONFIG_PATH)
        if not config.has_section("window"):
            config.add_section("window")
        if not config.has_section("sound"):
            config.add_section("sound")
        if not config.has_section("game"):
            config.add_section("game")

        config.set("window", "width", str(self.width))
        config.set("window", "height", str(self.height))
        config.set("window", "fullscreen", str(self.fullscreen))
        config.set("sound", "muted", str(self.sound_muted))
        config.set("sound", "volume", str(self.volume))
        config.set("game", "difficulty", self.difficulty)

        with open(CONFIG_PATH, "w") as cfgfile:
            config.write(cfgfile)

    def set_difficulty(self, _label: str, difficulty: str):
        """
        Update game difficulty and adjust the number of enemies accordingly.
        Saves the new difficulty into the config file.
        """
        self.difficulty = difficulty
        if difficulty == "Easy":
            self.enemies = 100
        elif difficulty == "Normal":
            self.enemies = 25
        else:
            self.enemies = 40
        print(f"Difficulty set to: {difficulty}")
        self.save_config()

    def get_difficulty(self):
        """Return the current difficulty string."""
        return self.difficulty

    def start_console(self):
        """
        Launch the Console window in a separate daemon thread if not already created.
        Prevents multiple console windows from being spawned.
        """
        if self.createdConsole == 1:
            if self.console_process is not None and not self.console_process.is_alive():
                self.createdConsole = 0
                self.console_process = None

        if self.createdConsole == 0:
            self.createdConsole = 1
            p = threading.Thread(
                target=console_process,
                args=(
                    self.sound_muted,
                    self.width,
                    self.height,
                    self.enemies,
                ),
                daemon=True
            )
            p.start()
            self.console_process = p

    def draw_menu(self):
        """
        Draw the main menu and settings menu, handling events and keeping
        the mute/unmute selector synchronized with Console.default_sound_muted.
        """
        pg.mixer.init()

        main_menu = pm.Menu(
            title=self.title,
            width=self.width,
            height=self.height,
            theme=self.custom_theme
        )
        settings_menu = pm.Menu('Settings', self.width, self.height, theme=self.custom_theme)

        # 1) Prepare pairs for the "Mute menu music" selector
        list_sound_status = [('Off', False), ('On', True)]
        sound_values = [pair[1] for pair in list_sound_status]  # -> [False, True]

        # 2) Read from config in case the console hasn't launched yet
        saved_sound_status = config.getboolean("sound", "muted", fallback=False)

        # 3) Determine the current boolean mute state:
        #   - If console_module.default_sound_muted is already bool, use it
        #   - Otherwise, use saved_sound_status from config
        if isinstance(console_module.default_sound_muted, bool):
            current_sound = console_module.default_sound_muted
        else:
            current_sound = saved_sound_status

        try:
            initial_index = sound_values.index(current_sound)

        except ValueError:
            # Fallback to "Off" if somehow neither is found
            initial_index = sound_values.index(False)

        # 4) Create the selector for Mute/Unmute
        self.status_music = settings_menu.add.selector(
            'Mute menu music:',
            list_sound_status,
            default=initial_index,
            onchange=self.set_sound_status
        )

        # Create the fullscreen toggle selector
        self.fullscreen_status = settings_menu.add.selector(
            'Fullscreen:',
            [('Off', False), ('On', True)],
            onchange=self.set_fullscreen
        )
        # Create the volume slider, disabled if muted
        self.volume_slider = settings_menu.add.range_slider(
            title="Volume",
            default=self.volume,
            range_values=(0.0, 1.0),
            increment=0.05,
            onchange=self.on_volume_change
        )

        self.volume_slider.readonly = self.sound_muted


        # Create the difficulty selector
        list_difficulty = [('Easy', 'Easy'), ('Normal', 'Normal'), ('Hard', 'Hard')]
        difficulty_values = [d[1] for d in list_difficulty]
        saved_difficulty = config.get("game", "difficulty", fallback="Normal")
        diff_index = difficulty_values.index(saved_difficulty) if self.check_play_game == 0 else 1

        settings_menu.add.selector(
            'Select difficulty:',
            list_difficulty,
            default=diff_index,
            onchange=self.set_difficulty,
        )

        # Button to open file dialog for spaceship selection
        settings_menu.add.button("Choose entities", self.choose_spaceship)
        settings_menu.add.button('Back', pm.events.BACK)

        # Main menu buttons
        main_menu.add.button('Play', self.start_game)
        main_menu.add.button('Settings', settings_menu)
        main_menu.add.button('Exit', pm.events.EXIT, font_color=WHITE)

        # Play background music if not muted
        if not self.sound_muted or console_module.default_sound_muted is False:
            pg.mixer.music.load("sound/menu_music/stellar-discovery-219109.mp3")
            pg.mixer.music.set_volume(self.volume)
            pg.mixer.music.play(0)

        # Immediately set selector value to avoid a visual glitch
        self.status_music.set_value(initial_index)
        self.volume_slider.readonly = (True if current_sound else False)

        if not self.volume_slider.readonly:
            pg.mixer_music.play(0)

        # Main loop to handle events and update menus
        prev_sound_state = current_sound
        while True:
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()
                if event.type == pg.KEYDOWN and event.key == pg.K_2:
                    self.start_console()

            # ==== Synchronize the selector only if the mute state changed ====
            new_sound_state = (
                console_module.default_sound_muted
                if isinstance(console_module.default_sound_muted, bool)
                else saved_sound_status
            )
            if new_sound_state != prev_sound_state:
                try:
                    idx = sound_values.index(new_sound_state)
                except ValueError:
                    idx = sound_values.index(False)
                self.status_music.set_value(idx)
                self.volume_slider.readonly = new_sound_state

                if not new_sound_state:
                    pg.mixer.music.set_volume(self.volume)
                    pg.mixer.music.play(-1)
                else:
                    pg.mixer.music.stop()

                prev_sound_state = new_sound_state



            # ==== Update background and draw menus ====
            self.bg.update()
            self.bg.draw()
            main_menu.update(events)
            main_menu.draw(self.screen)
            pg.display.flip()

    def start_game(self):
        """
        Fill the screen black, increment the play counter, call the start_game_callback,
        and pause/unpause menu music depending on mute state.
        """
        self.screen.fill(BLACK)
        pg.display.update()
        self.check_play_game += 1
        print(f"Start new game : {self.check_play_game}")
        self.start_game_callback()
        if self.sound_muted:
            pg.mixer.music.pause()
        else:
            pg.mixer.music.unpause()

    def set_sound_status(self, _label, mute: bool) -> bool:
        """
        Called when the user changes the mute selector in the settings menu.
        Updates self.sound_muted, pauses or resumes music, saves to config,
        and updates the global console_module.default_sound_muted.
        """
        self.sound_muted = mute
        if self.sound_muted:
            pg.mixer.music.pause()
        else:
            if not pg.mixer.music.get_busy():
                pg.mixer.music.load("sound/menu_music/stellar-discovery-219109.mp3")
                pg.mixer.music.play(-1)
            else:
                pg.mixer.music.unpause()
            pg.mixer.music.set_volume(self.volume)


        if self.volume_slider:
            self.volume_slider.readonly = self.sound_muted

        # Save new mute status to config file
        self.save_config()

        # Update the global variable in console.py so the console window sees the change
        console_module.default_sound_muted = mute


        return self.sound_muted

    def on_volume_change(self, value: float):
        """
        Adjust the music volume if not muted and save the volume setting to config.
        """
        self.volume = value
        if not self.sound_muted:
            pg.mixer.music.set_volume(self.volume)
        self.save_config()

    def set_fullscreen(self, _label: str, fullscreen: bool) -> bool:
        """
        Toggle fullscreen mode for the game window and save that preference to config.
        """
        self.fullscreen = fullscreen
        if fullscreen:
            self.screen = pg.display.set_mode((self.width, self.height), pg.FULLSCREEN)
        else:
            self.screen = pg.display.set_mode((self.width, self.height))
        self.bg.screen = self.screen
        print(f"Fullscreen mode is now {'enabled' if fullscreen else 'disabled'}.")
        self.save_config()
        return fullscreen

    def choose_spaceship(self):
        """
        Open the file dialog to let the user pick a custom spaceship image.
        Store the resulting file path in self.spaceship_path.
        """
        selected = open_filedialog("")
        if selected:
            self.spaceship_path = selected
            print(f"Spaceship image set to: {self.spaceship_path}")
