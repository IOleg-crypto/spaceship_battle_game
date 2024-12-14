import pygame as pg
import configparser as cfgp


WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)

pg.font.init()
FONT = pg.font.SysFont("Arial", 24)

config = cfgp.ConfigParser()
config.read("config/config.cfg")

class Console:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.lines = []  # Stores console output
        self.input_text = ""  # Current input text
        self.is_open = False  # Console visibility
        self.max_lines = 10  # Max number of visible lines

    def toggle(self):
        """Toggle console visibility."""
        self.is_open = not self.is_open

    def add_line(self, text):
        """Add a line to the console output."""
        self.lines.append(text)
        if len(self.lines) > self.max_lines:
            self.lines.pop(0)

    def handle_event(self, event):
        """Handle keyboard input for the console."""
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            elif event.key == pg.K_RETURN:
                # Execute the command
                self.add_line(f"> {self.input_text}")
                self.execute_command(self.input_text)
                self.input_text = ""
            elif event.unicode:  # Add character to input text
                self.input_text += event.unicode

    def execute_command(self, command):
        """Execute a console command."""
        if command == "clear":
            self.lines = []
        elif command.startswith("echo "):
            self.add_line(command[5:])
        else:
            self.add_line(f"Unknown command: {command}")

    def draw(self, surface):
        """Render the console on the screen."""
        if not self.is_open:
            return

        # Draw console background
        pg.draw.rect(surface, GRAY, (0, 0, self.width, self.height))
        pg.draw.line(surface, GREEN, (0, self.height), (self.width, self.height), 2)

        # Draw console lines
        y_offset = 5
        for line in self.lines:
            text_surface = FONT.render(line, True, WHITE)
            surface.blit(text_surface, (5, y_offset))
            y_offset += 20

        # Draw input text
        input_surface = FONT.render(f"> {self.input_text}", True, WHITE)
        surface.blit(input_surface, (5, y_offset))