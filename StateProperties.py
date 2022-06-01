from dataclasses import dataclass, field

from constants import ROOM_TEMPERATURE


@dataclass
class StateProperties:
    temperature: float
    _temperature: float = field(init=False, repr=False, default=ROOM_TEMPERATURE)
    is_burning: bool = False

    @property
    def temperature(self):
        return self._temperature

    @temperature.setter
    def temperature(self, val):
        if type(val) is property:
            # initial value not specified, use default
            val = StateProperties._temperature
        # if val < 0:
        #     assert(val >= 0)
        self._temperature = val
