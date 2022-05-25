from ursina import *
from MaterialProperties import MaterialProperties
from StateProperties import StateProperties
from ColorToTemperature import ColorToTemperature


class Voxel(Button):
    def __init__(self, position, color_hsv):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            origin_y=.5,
            texture='white_cube',
            # color=color.color(*color_hsv),
            color=color.rgb(*ColorToTemperature().convert_K_to_RGB(290)),
            highlight_color=color.color(color_hsv[0], min(1, color_hsv[1]*1.3), 1),
        )


    # def input(self, key):
    #     if self.hovered:
    #         if key == 'left mouse down':
    #             voxel = Voxel(position=self.position + mouse.normal)
    #
    #         if key == 'x':
    #             destroy(self)


class Cell:
    def __init__(self, position, material_properties: MaterialProperties, state: StateProperties):
        self.voxel = Voxel(position, material_properties.color)
        self.material_properties = material_properties
        self.state = state
        self.next_state = state

    def toString(self):
        return str(self.material_properties.id)
