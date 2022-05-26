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
