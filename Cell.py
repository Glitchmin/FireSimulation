from ursina import *
from MaterialProperties import MaterialProperties
from StateProperties import StateProperties
from ColorToTemperature import ColorToTemperature
from constants import BLOCK_SIZE_M


class Voxel(Button):
    fire_color = color.color(0, 0.8, 1)
    flame_color = color.color(0, 0.8, 1, 0.5)

    def __init__(self, position, color_hsv):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            origin_y=.5,
            texture='white_cube',
            color=color.color(*color_hsv),
            # color=color.rgb(*ColorToTemperature().convert_K_to_RGB(290)),
            highlight_color=color.color(color_hsv[0], min(1, color_hsv[1] * 1.3), 1),
        )


class Cell(Entity):
    def __init__(self, position, material_properties: MaterialProperties, state: StateProperties, **kwargs):
        super().__init__(**kwargs)
        self.material_properties = material_properties
        self.state = state
        self.next_state = copy(state)
        self.neighbors: [Cell] = []
        self.voxel = None
        self.position = position
        if not self.material_properties.is_invisible():
            self.voxel = Voxel(position, material_properties.color)

    def to_string(self):
        return str(self.material_properties.id)

    def input(self, key):
        if key == 'g':
            self.voxel.color = color.rgb(*ColorToTemperature().convert_K_to_RGB(self.state.temperature))

    def update_voxel(self, thermal_mode):
        if thermal_mode:
            if not self.material_properties.is_invisible():
                self.voxel.color = color.rgb(*ColorToTemperature().convert_K_to_RGB(self.state.temperature))
        else:
            if self.state.is_burning:
                if self.voxel is None:
                    self.voxel = Voxel(self.position, self.material_properties.color)
                if self.material_properties.is_transparent():
                    self.voxel.color = Voxel.flame_color
                else:
                    self.voxel.color = Voxel.fire_color
            elif not self.material_properties.is_invisible():
                self.voxel.color = color.color(*self.material_properties.color)
            elif self.state.smoke_saturation > 0:
                if self.voxel is None:
                    self.voxel = Voxel(self.position, self.material_properties.color)

                self.voxel.color = color.color(0, 0, 0.5, self.state.smoke_saturation)

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

    def calc_next_state(self, time_s):
        self.next_state.is_burning = self.state.temperature >= self.material_properties.autoignition_temp

        self.calculate_conduction(time_s)
        self.calculate_smoke(time_s)

    def calculate_smoke(self, time_s):
        for neighbor in self.neighbors:
            if self.material_properties.id != 0 and neighbor.position[1] > self.position[1] and \
                    neighbor.material_properties.id == 0 and self.state.is_burning:
                neighbor.next_state.smoke_saturation += self.material_properties.smoke_generation_s * time_s
            if self.material_properties.id == 0 and neighbor.position[1] > self.position[1] and \
                    neighbor.material_properties.id == 0:
                neighbor.next_state.smoke_saturation += self.state.smoke_saturation
                self.next_state.smoke_saturation -= self.state.smoke_saturation

    def calculate_conduction(self, time_s):
        heat = 0
        for neighbor in self.neighbors:
            if neighbor is not None:
                R1 = BLOCK_SIZE_M / 2 / self.material_properties.conductivity
                R2 = BLOCK_SIZE_M / 2 / neighbor.material_properties.conductivity
                R = R1 + R2
                U = 1 / R
                q = U * BLOCK_SIZE_M * BLOCK_SIZE_M * (neighbor.state.temperature - self.state.temperature)
                heat += q
        heat *= time_s
        self.next_state.temperature += heat / (
                self.material_properties.specific_heat * self.material_properties.density)
        # print(self.next_state.temperature)
