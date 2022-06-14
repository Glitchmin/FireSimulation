from math import inf
from typing import Tuple

from Cell import Cell
from MaterialProperties import MaterialProperties
from StateProperties import StateProperties


class CellGenerator:
    def __init__(self):
        self._building_material_id = 1
        self.empty_material = 0
        self.material_defs = {
            0: MaterialProperties(0, "air", color=(0, 0, 0, 0.01), specific_heat=1.,
                                  density=1.225,
                                  conductivity=0.025,
                                  autoignition_temp=inf, smoke_generation_s=0.0, emissivity=0.0),
            1: MaterialProperties(1, "wood", color=(0.5, 0.35, 0.28), specific_heat=2400, density=500, conductivity=0.2,
                                  autoignition_temp=273 + 250, smoke_generation_s=1 / 10, emissivity=0.94),
            2: MaterialProperties(2, "iron", color=(0, 0.05, 0.9), specific_heat=440, density=7800, conductivity=50,
                                  autoignition_temp=273 + 1315, smoke_generation_s=1 / 60, emissivity=0.24),
            3: MaterialProperties(3, "brick", color=(354, 0.6, 0.99), specific_heat=880, density=1500,
                                  conductivity=0.9, autoignition_temp=4000, smoke_generation_s=0.0, emissivity=0.93)

        }

    @property
    def building_material_id(self):
        return self._building_material_id

    @building_material_id.setter
    def building_material_id(self, new_id):
        if new_id in self.material_defs.keys():
            self._building_material_id = new_id

    def get_cell(self, position: Tuple, material_id: int = None):
        if material_id is None:
            material_id = self.building_material_id

        # return Cell(position, self.material_defs[material_id], StateProperties(temperature=273+position[0]*30+position[2]*100))
        return Cell(position, self.material_defs[material_id], StateProperties())
