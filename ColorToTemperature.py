from constants import ROOM_TEMPERATURE
from constants import MAX_TEMPERATURE


class ColorToTemperature:
    def __init__(self, min_: float = ROOM_TEMPERATURE, max_: float = MAX_TEMPERATURE):
        self.min = min_
        self.max = max_

    def change_colors(self):
        pass
