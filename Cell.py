from ursina import *
from MaterialProperties import MaterialProperties
from StateProperties import StateProperties
from ColorToTemperature import ColorToTemperature
from constants import BLOCK_SIZE_M


class Voxel(Button):
    def __init__(self, position, color_hsv):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            origin_y=.5,
            texture='white_cube',
            color=color.color(*color_hsv),
            # color=color.rgb(*ColorToTemperature().convert_K_to_RGB(290)),
            highlight_color=color.color(color_hsv[0], min(1, color_hsv[1]*1.3), 1),
        )




class Cell(Entity):
    def __init__(self, position, material_properties: MaterialProperties, state: StateProperties, **kwargs):
        super().__init__(**kwargs)
        self.material_properties = material_properties
        self.state = state
        self.next_state = state
        self.neighbors = []
        self.voxel = Voxel(position, material_properties.color)

    def to_string(self):
        return str(self.material_properties.id)

    def input(self, key):
        if key == 'g':
            self.voxel.color = color.rgb(*ColorToTemperature().convert_K_to_RGB(self.state.temperature))

    def update_voxel(self, thermal_mode):
        if thermal_mode:
            self.voxel.color = color.rgb(*ColorToTemperature().convert_K_to_RGB(self.state.temperature))
        else:
            self.voxel.color = color.color(*self.material_properties.color)

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

    def calc_next_state(self, time_s):
        heat = 0
        for neighbor in self.neighbors:
            R1 = BLOCK_SIZE_M/2 / self.material_properties.conductivity
            R2 = BLOCK_SIZE_M/2 / neighbor.material_properties.conductivity
            R = R1 + R2
            U = 1 / R
            q = U * BLOCK_SIZE_M * BLOCK_SIZE_M * (self.state.temperature - neighbor.state.temperature)
            heat += q
        heat *= time_s
        self.state.temperature += heat / self.material_properties.specific_heat
