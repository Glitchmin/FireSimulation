from dataclasses import dataclass
from typing import Tuple


@dataclass
class MaterialProperties:
    id: int
    name: str
    specific_heat: float
    color: Tuple
