from constants import ROOM_TEMPERATURE
from constants import MAX_TEMPERATURE
import math


class ColorToTemperature:
    def __init__(self, min_: float = ROOM_TEMPERATURE, max_: float = MAX_TEMPERATURE):
        self.min = min_
        self.max = max_

    def convert_K_to_RGB(self, colour_temperature):
        x = colour_temperature / (self.max - self.min)
        if x < 0:
            return 0, 0, 0

        r = round(255 * math.sqrt(x))
        g = round(255 * math.pow(x, 3))
        if math.sin(2 * math.pi * x) >= 0:
            b = round(255 * (math.sin(2 * math.pi * x)))
        else:
            b = 0

        return r, g, b


