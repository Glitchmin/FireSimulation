from dataclasses import dataclass

from constants import ROOM_TEMPERATURE


@dataclass
class StateProperties:
    temperature: float = ROOM_TEMPERATURE
    is_burning: bool = False
    smoke_saturation: float = 0.0
