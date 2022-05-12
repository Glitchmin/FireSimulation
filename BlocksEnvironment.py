from ursina import *

from Cell import Cell
from CellGenerator import CellGenerator


class BlocksEnvironment(Entity):
    def __init__(self, x_size: int, y_size: int, z_size: int, **kwargs):
        super().__init__(**kwargs)
        self.cell_generator = CellGenerator()
        self.cells = [[[None for _ in range(z_size)] for _ in range(y_size)] for _ in range(x_size)]
        self.size = (x_size, y_size, z_size)
        for z in range(z_size):
            for x in range(x_size):
                self.create_cell((x, 0, z))

    def create_cell(self, position):
        position = tuple([int(a) for a in position])
        for pos1d, size1d in zip(position, self.size):
            if not (0 <= pos1d < size1d):
                return
        self.cells[position[0]][position[1]][position[2]] = self.cell_generator.get_cell(position)

    def remove_cell(self, position):
        position = [int(a) for a in position]
        for pos1d, size1d in zip(position, self.size):
            if not (0 <= pos1d < size1d):
                return

        if self.cells[position[0]][position[1]][position[2]] is not None:
            destroy(self.cells[position[0]][position[1]][position[2]].voxel)
            self.cells[position[0]][position[1]][position[2]] = None

    def input(self, key):
        # pass
        # if mouse.world_point:
        #     print(mouse.world_point)
        #     print(camera.world_position)
        #     print(camera.forward)
        if key == 'left mouse down':
            if mouse.world_point is not None:
                hit_info = raycast(camera.world_position, mouse.world_point - camera.world_position, distance=inf)
                if hit_info.hit:
                    position = hit_info.entity.position + hit_info.normal
                    self.create_cell(position)
        if key == 'x':
            if mouse.world_point is not None:
                hit_info = raycast(camera.world_position, mouse.world_point - camera.world_position, distance=inf)
                if hit_info.hit:
                    position = hit_info.entity.position
                    self.remove_cell(position)