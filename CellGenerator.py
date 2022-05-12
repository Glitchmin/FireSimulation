from typing import Tuple

from Cell import Cell
from MaterialProperties import MaterialProperties


class CellGenerator:
    def __init__(self):
        self.default_material_id = 1
        self.material_defs = {1: MaterialProperties(1, 400, (100, 0.3, 0.9))}

    def get_cell(self, position: Tuple, material_id: int = None):
        if material_id is None:
            material_id = self.default_material_id

        return Cell(position, self.material_defs[material_id])
