from ursina import *

from MaterialProperties import MaterialProperties


class Voxel(Button):
    def __init__(self, position, color_hsv):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            origin_y=.5,
            texture='white_cube',
            color=color.color(*color_hsv),
            highlight_color=color.lime,
        )

    # def input(self, key):
    #     if self.hovered:
    #         if key == 'left mouse down':
    #             voxel = Voxel(position=self.position + mouse.normal)
    #
    #         if key == 'x':
    #             destroy(self)


class Cell:
    def __init__(self, position, material_properties: MaterialProperties):
        self.voxel = Voxel(position, material_properties.color)
        self.material_properties = material_properties
