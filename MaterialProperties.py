from dataclasses import dataclass
from typing import Tuple


@dataclass
class MaterialProperties:
    id: int
    name: str
    specific_head: float
    color: Tuple
