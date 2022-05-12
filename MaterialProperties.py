from typing import Tuple


class MaterialProperties:
    def __init__(self, id:int, specific_heat, color: Tuple):
        self.id = id
        self.specific_head = specific_heat
        self.color = color
