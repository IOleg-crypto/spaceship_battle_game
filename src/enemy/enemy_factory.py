import random
from entities import Enemy

def create_enemies(screen, image_paths, num):
    return [Enemy(screen, random.choice(image_paths)) for _ in range(num)]

def set_difficulty(screen, difficulty: str):
    width, height = screen
    base = {"Easy": 10, "Normal": 25, "Hard": 40}
    extra = 10 if width > 800 or height > 600 else 0
    return base.get(difficulty, 40) + extra