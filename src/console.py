"""Console for spaceship game."""

import tkinter as tk


class Console(tk.Tk):

    def __init__(self, sound_muted: bool):
        super().__init__()
        self.title("Console")
        self.sound_muted = sound_muted

        # Set fixed window size and prevent resizing
        self.geometry("800x600")  # Example size, can be adjusted
        self.resizable(True, True)

        self.config(bg="gray")
        self.wm_attributes("-transparentcolor", "gray")  # Make the black color transparent

        # Output window (Text)
        self.text_widget = tk.Text(self, height=25, width=110, bg="gray", fg="white", font=("Courier New", 9))
        self.text_widget.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.text_widget.config(state=tk.DISABLED)  # Make it read-only

        # Input field (Entry) - for command input
        self.entry = tk.Entry(self, width=80, bg="gray", fg="white", font=("Courier New", 9))
        self.entry.pack(padx=5, pady=2, fill=tk.X)
        self.entry.bind("<Return>", self.execute_command)  # Execute command on Enter

    def execute_command(self, event):
        command = self.entry.get()
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.insert(tk.END, f"> {command}\n")
        self.entry.delete(0, tk.END)

        commands = {
            "m_soundmute 1": lambda: self.toggle_sound(True),
            "m_soundmute 0": lambda: self.toggle_sound(False),
            "cls": lambda: self.clear_text(),
        }

        result = commands.get(command, lambda: f"Unknown command: {command}")()

        self.text_widget.insert(tk.END, f"{result}\n")
        self.text_widget.config(state=tk.DISABLED)
        self.text_widget.see(tk.END)

    def toggle_sound(self, mute):
        self.sound_muted = mute
        return "Sound muted." if mute else "Sound unmuted."

    def clear_text(self):
        self.text_widget.delete("1.0", tk.END)
