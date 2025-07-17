from menu import MainMenu

def set_difficulty(num_enemies: int, screen) -> int:
    if MainMenu.get_difficulty == "Easy":
        num_enemies = 10
        if screen[0] > 800 or screen[1] > 600:
            num_enemies = 20
    elif MainMenu.get_difficulty == "Normal":
        num_enemies = 25
        if screen[0] > 800 or screen[1] > 600:
            num_enemies = 30
    else:
        num_enemies = 40
        if screen[0] > 800 or screen[1] > 600:
            num_enemies = 60
    return num_enemies