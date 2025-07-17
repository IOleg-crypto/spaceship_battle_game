"""main.py - main game functionality"""

from game.game import Game
import random
import pygame as pg

def main():
    pg.init()
    pg.mixer.init()
    game = Game()
    game.start_menu()
    pg.quit()


"""Start game , default shit"""
if __name__ == "__main__":
    main()
