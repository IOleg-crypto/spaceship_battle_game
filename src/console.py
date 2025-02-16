"""Console for spaceship game."""

import pygame as pg
import tkinter as tk
import configparser as cfg
import ctypes

config = cfg.ConfigParser()
config.read("config/config.cfg")

"""For DPI"""
ctypes.windll.shcore.SetProcessDpiAwareness(1)




class Console(tk.Tk):
    def __init__(self, sound_muted: bool):
        super().__init__()
        self.title("Console")
        self.sound_muted = sound_muted

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
        self.text_widget.config(state=tk.NORMAL)  # Enable writing on startup

        # Show startup text
        startup_text = (
            "SpaceShip Battle! Build 1.0\n"
            "Author: I#Oleg\n"
            "Version: 1.0\n"
            "Date compiled: 15.02.2025\n"
        )
        self.text_widget.insert(tk.END, startup_text)
        self.text_widget.config(state=tk.DISABLED)  # Make it read-only again

        # Input field (Entry)
        self.entry = tk.Entry(self, width=80, bg="gray", fg="white", font=("Courier New", 9))
        self.entry.pack(padx=5, pady=2, fill=tk.X)
        self.entry.bind("<Return>", self.execute_command)
        self.entry.bind("<KeyRelease>", self.auto_complete)  # Auto-complete event

        # Available commands for auto-completion
        self.commands = ["sound 1", "sound 0", "cls", "help"]

        self.deiconify()  # Show the console window

    def execute_command(self, event):
        command = self.entry.get()
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.insert(tk.END, f"> {command}\n")
        self.entry.delete(0, tk.END)

        # Define possible commands
        commands = {
            "sound 1": lambda: self.toggle_sound(True),
            "sound 0": lambda: self.toggle_sound(False),
            "cls": lambda: self.clear_text(),
            "help": lambda: "Available commands: " + ", ".join(self.commands),
        }

        # Execute the command or show an unknown command message
        result = commands.get(command, lambda: f"Unknown command: {command}")()

        self.text_widget.insert(tk.END, f"{result}\n")
        self.text_widget.config(state=tk.DISABLED)
        self.text_widget.see(tk.END)

    def auto_complete(self, event):
        """Auto-complete the input field based on available commands."""
        typed_text = self.entry.get()
        if typed_text:  # Only suggest if there is input
            for command in self.commands:
                if command.startswith(typed_text):
                    self.entry.delete(0, tk.END)
                    self.entry.insert(0, command)
                    self.entry.icursor(len(typed_text))  # Keep cursor at user input
                    break  # Stop at the first match

    def toggle_sound(self, mute: bool):
        """Toggle the mute/unmute state."""
        self.sound_muted = mute
        pg.mixer.music.set_volume(0 if self.sound_muted else 1)  # Mute or unmute the music
        self.update_sound_state()

    def update_sound_state(self):
        """Update the display of the sound state in the console."""
        state = "Muted" if self.sound_muted else "Unmuted"
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.insert(tk.END, f"Sound is {state}\n")
        self.text_widget.config(state=tk.DISABLED)

    def clear_text(self):
        """Clear the output text area."""
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.delete("1.0", tk.END)

        # Reinsert startup text after clearing
        startup_text = (
            "SpaceShip Battle! Build 1.0\n"
            "Author: I#Oleg\n"
            "Version: 1.0\n"
            "Date compiled: 15.02.2025\n"
        )
        self.text_widget.insert(tk.END, startup_text)
        self.text_widget.config(state=tk.DISABLED)
