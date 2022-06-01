from math import inf
from typing import Tuple

from Cell import Cell
from MaterialProperties import MaterialProperties
from StateProperties import StateProperties


class CellGenerator:
    def __init__(self):
        self._default_material_id = 1
        self.material_defs = {
            0: MaterialProperties(0, "air", color=(0, 0, 0, 0), specific_heat=1.0, density=1.225, conductivity=0.025,
                                  autoignition_temp=inf),
            1: MaterialProperties(0, "air", color=(100, 0.3, 0.9), specific_heat=2400, density=500, conductivity=0.2,
                                  autoignition_temp=273+250),
            # 2: MaterialProperties(2, "name_2", 1000, (200, 0.5, 0.9)),
            # 3: MaterialProperties(3, "name_3", 1000, (0, 0.0, 0.5, 0.5)),
            # 4: MaterialProperties(4, "name_4", 1000, (0, 0.7, 0.9, 0.8))
        }

    @property
    def default_material_id(self):
        return self._default_material_id

    @default_material_id.setter
    def default_material_id(self, new_id):
        if new_id in self.material_defs.keys():
            self._default_material_id = new_id

    def get_cell(self, position: Tuple, material_id: int = None):
        if material_id is None:
            material_id = self.default_material_id

        # return Cell(position, self.material_defs[material_id], StateProperties(temperature=273+position[0]*30+position[2]*100))
        return Cell(position, self.material_defs[material_id], StateProperties())
