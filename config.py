from enum import Enum

import numpy as np


class Colour(Enum):
    RED = (240, 10, 10)
    WHITE = (240, 240, 240)
    BLACK = (30, 30, 30)
    BLUE = (10, 10, 240)
    YELLOW = (255, 255, 0)
    CYAN = (0, 255, 255)
    GREY = (200, 200, 200)
    METAL_GREY = (90, 90, 90)
    OAK_BROWN = (230, 190, 145)


MOVEMENT_QUANTUM = 200

I_a = 0.7
I_d = 1.2
I_s = 1.3

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_CENTRE = np.array([SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 0])
