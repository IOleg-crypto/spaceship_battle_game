"""Console for spaceship game with autocomplete."""

import pygame as pg
import tkinter as tk
import configparser as cfg
import ctypes




config = cfg.ConfigParser()
config.read("config/config.cfg")

"""For DPI"""
ctypes.windll.shcore.SetProcessDpiAwareness(1)


default_index = 0


class Console(tk.Toplevel):
    def __init__(self, sound_muted: bool, screen_height: int, screen_width: int, enemies: int):
        super().__init__()
        self.title("Console")
        self.sound_muted = sound_muted
        self.screen_height = screen_height
        self.screen_width = screen_width
        self.enemies = enemies
        self.number = 0

        """To take control on main menu"""
        global default_index


        # Initialize pygame mixer
        pg.init()
        pg.mixer.init()

        # Set fixed window size and prevent resizing
        self.geometry("800x600")
        self.resizable(False, False)
        self.config(bg="gray")
        self.wm_attributes("-alpha", 0.9)

        # Output window (Text)
        self.text_widget = tk.Text(self, height=15, width=110, bg="gray", fg="white", font=("Courier New", 9))
        self.text_widget.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.text_widget.config(state=tk.NORMAL)

        # Show startup text
        startup_text = (
            "SpaceShip Battle! Build 1.3\n"
            "Author: I#Oleg\n"
            "Version: 1.3\n"
            "Date compiled: 01.06.2025\n"
        )
        self.text_widget.insert(tk.END, startup_text)
        self.text_widget.config(state=tk.DISABLED)

        # Input field (Entry)
        self.entry = tk.Entry(self, width=80, bg="gray", fg="white", font=("Jetbrains Mono", 9))
        self.entry.pack(padx=5, pady=2, fill=tk.X)
        self.entry.bind("<Return>", self.execute_command)
        self.entry.bind("<KeyRelease>", self.show_suggestions)
        self.entry.bind("<Tab>", self.autocomplete)

        # Listbox for autocomplete

        self.listbox = tk.Listbox(self, bg="gray", fg="white", font=("Arial", 9), height=3)
        self.listbox.pack(padx=5, pady=1, fill=tk.X)
        self.listbox.bind("<<ListboxSelect>>", self.select_from_listbox)

        # Available commands
        self.commands = ["sound 1", "sound 0", "cls", "enemies" , "help"]
        self.suggestion_index = -1  # Tracks the selected suggestion in Listbox

        self.deiconify()

    def execute_command(self, event):
        """Handles execution of entered commands."""
        command = self.entry.get().strip()
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.insert(tk.END, f"> {command}\n")
        self.entry.delete(0, tk.END)
        self.listbox.delete(0, tk.END)  # Clear suggestion box

        # Handle "enemies {number}" separately
        if command.startswith("enemies "):
            try:
                number = int(command.split(" ")[1])  # Extract number
                self.enemies = number
                result = f"Enemies set to {self.enemies}"
            except (IndexError, ValueError):
                result = "Invalid usage! Use: enemies {number}"
        else:
            # Static commands dictionary
            commands = {
                "sound 0": lambda: self.toggle_sound(True),
                "sound 1": lambda: self.toggle_sound(False),
                "cls": self.clear_text,
                "help": lambda: "Available commands: " + ", ".join(self.commands),
            }

            result = commands.get(command, lambda: f"Unknown command: {command}")()

        self.text_widget.insert(tk.END, f"{result}\n")
        self.text_widget.config(state=tk.DISABLED)
        self.text_widget.see(tk.END)

    def show_suggestions(self, event):
        """Displays autocomplete suggestions in the listbox."""
        value = self.entry.get().strip().lower()
        self.listbox.delete(0, tk.END)

        if not value:
            return  # Don't show suggestions when input is empty

        matches = [cmd for cmd in self.commands if cmd.startswith(value)]
        for match in matches:
            self.listbox.insert(tk.END, match)

        self.suggestion_index = -1  # Reset selection

    def autocomplete(self, event):
        """Fills the entry with the first suggestion on Tab key."""
        if self.listbox.size() > 0:
            selected = self.listbox.get(0)
            self.entry.delete(0, tk.END)
            self.entry.insert(0, selected)
            self.listbox.delete(0, tk.END)  # Hide suggestions
        return "break"  # Prevent default Tab behavior

    def select_from_listbox(self, event):
        """Handles selection from the autocomplete listbox."""
        selected = self.listbox.get(tk.ACTIVE)
        self.entry.delete(0, tk.END)
        self.entry.insert(0, selected)
        self.listbox.delete(0, tk.END)  # Hide suggestions

    def toggle_sound(self, mute: bool):
        """Toggle sound on/off and update shared state and config."""
        global default_index  # <-- додаємо
        self.sound_muted = mute
        pg.mixer.music.set_volume(0 if mute else 1)

        # Update config and save to file
        if not config.has_section("sound"):
            config.add_section("sound")
        config.set("sound", "muted", str(mute))
        with open("config/config.cfg", "w") as configfile:
            config.write(configfile)

        # Оновлюємо глобальну змінну, щоб меню побачило зміни
        default_index = 1 if mute else 0

        return f"Sound {'muted' if mute else 'unmuted'}"

    def get_sound_muted(self):
        return self.sound_muted

    def update_sound_state(self):
        """Update sound state display."""
        state = None
        if not self.sound_muted:
            state = "Unmuted"
        else:
            state = "Muted"
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.insert(tk.END, f"Sound is {state}\n")
        self.text_widget.config(state=tk.DISABLED)

    def clear_text(self):
        """Clear the console output."""
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.delete("1.0", tk.END)
        startup_text = (
            "SpaceShip Battle! Build 1.3\n"
            "Author: I#Oleg\n"
            "Version: 1.3\n"
            "Date compiled: 01.06.2025\n"
        )
        self.text_widget.insert(tk.END, startup_text)
        self.text_widget.config(state=tk.DISABLED)
