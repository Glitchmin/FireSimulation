import string
from typing import Union

from RoomSaver import RoomSaver
from ursina import *

from Cell import Cell
from CellGenerator import CellGenerator


class BlocksEnvironment(Entity):
    def __init__(self, x_size: int, y_size: int, z_size: int, **kwargs):
        super().__init__(**kwargs)
        self.cell_generator = CellGenerator()
        self.cells = [[[None for _ in range(z_size)] for _ in range(y_size)] for _ in range(x_size)]
        self.size = (x_size, y_size, z_size)
        self.thermal_camera_mode = False

        for x in range(x_size):
            for y in range(1, y_size):
                for z in range(z_size):
                    self.create_cell((x, y, z), self.cell_generator.empty_material)

        for z in range(z_size):
            for x in range(x_size):
                self.create_cell((x, 0, z))

        for z in range(z_size):
            for y in range(1, y_size):
                self.create_cell((0, y, z), material_id=3)
                self.create_cell((x_size - 1, y, z), material_id=3)

        for x in range(x_size):
            for y in range(1, y_size):
                # self.create_cell((x, y, 0), material_id=3)
                self.create_cell((x, y, z_size-1), material_id=3)

    def cell_at(self, position) -> Cell:
        position = [int(a) for a in position]
        return self.cells[position[0]][position[1]][position[2]]

    def create_cell(self, position, material_id: Union[int, None] = None):
        position = tuple([int(a) for a in position])
        for pos1d, size1d in zip(position, self.size):
            if not (0 <= pos1d < size1d):
                return
        if self.cells[position[0]][position[1]][position[2]] is not None:
            destroy(self.cells[position[0]][position[1]][position[2]].voxel)
            self.cells[position[0]][position[1]][position[2]] = None

        self.cells[position[0]][position[1]][position[2]] = self.cell_generator.get_cell(position, material_id)
        self.cells[position[0]][position[1]][position[2]].update_voxel(self.thermal_camera_mode)
        self.cells[position[0]][position[1]][position[2]].position = position

    def remove_cell(self, position):
        position = [int(a) for a in position]
        for pos1d, size1d in zip(position, self.size):
            if not (0 <= pos1d < size1d):
                return

        if self.cells[position[0]][position[1]][position[2]] is not None:
            destroy(self.cells[position[0]][position[1]][position[2]].voxel)
            self.create_cell(position, self.cell_generator.empty_material)

    def refresh_voxels(self):
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                for z in range(self.size[2]):
                    if self.cells[x][y][z] is not None:
                        self.cells[x][y][z].update_voxel(self.thermal_camera_mode)

    def switch_view_mode(self):
        self.thermal_camera_mode = not self.thermal_camera_mode
        self.refresh_voxels()

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
                    print(self.cell_at(position).material_properties.is_invisible(), self.cell_at(position).material_properties.is_transparent(), self.cell_at(position).material_properties.color)
                    self.remove_cell(position)

        if key == 'i':
            if mouse.world_point is not None:
                hit_info = raycast(camera.world_position, mouse.world_point - camera.world_position, distance=inf)
                if hit_info.hit:
                    position = hit_info.entity.position
                    print('T:', self.cell_at(position).state.temperature)
                    print('smoke:', self.cell_at(position).state.smoke_saturation)
                    # self.remove_cell(position)

        if key == 's' and held_keys['left control']:
            print("saving...")
            RoomSaver.save_room(self.cells)
            print("saving finished")

        if key == 'l' and held_keys['left control']:
            print("loading...")
            for i in range(len(self.cells)):
                for j in range(len(self.cells[i])):
                    for k in range(len(self.cells[i][j])):
                        if self.cells[i][j][k] is not None:
                            self.remove_cell([i, j, k])
            RoomSaver.load_room(self.cells, self.cell_generator)
            print("loading finished")

        for id in self.cell_generator.material_defs.keys():
            if key == str(id):
                self.cell_generator.building_material_id = id
