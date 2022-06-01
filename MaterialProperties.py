from dataclasses import dataclass
from typing import Tuple


@dataclass
class MaterialProperties:
    id: int
    name: str
    color: Tuple
    specific_heat: float        # J/(K*kg)
    density: float              # kg/m^3
    conductivity: float         # W/(m*K)
    autoignition_temp: float    # K
    smoke_generation_s: float

    def is_transparent(self):
        return len(self.color) >= 4 and self.color[3] < 1

    def is_invisible(self):
        return len(self.color) >= 4 and self.color[3] == 0