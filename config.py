from enum import Enum


class Colour(Enum):
    RED = (240, 10, 10)
    WHITE = (240, 240, 240)
    BLACK = (30, 30, 30)
    BLUE = (10, 10, 240)
    GREEN = (0, 255, 0)
    YELLOW = (255, 255, 0)
    CYAN = (0, 255, 255)
    MAGENTA = (255, 0, 255)


SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
