from typing import Tuple

from Cell import Cell
from MaterialProperties import MaterialProperties


class CellGenerator:
    def __init__(self):
        self._default_material_id = 1
        self.material_defs = {1: MaterialProperties(1, "name_1", 400, (100, 0.3, 0.9)),
                              2: MaterialProperties(2, "name_2", 1000, (200, 0.5, 0.9)),
                              3: MaterialProperties(3, "name_3", 1000, (0, 0.0, 0.5, 0.5)),
                              4: MaterialProperties(4, "name_4", 1000, (0, 0.7, 0.9, 0.8))}

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

        return Cell(position, self.material_defs[material_id])
