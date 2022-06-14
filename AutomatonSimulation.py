import threading
from copy import copy

from ursina import *
from BlocksEnvironment import BlocksEnvironment
from Cell import Cell
import sys


class AutomatonSimulation(threading.Thread):
    def __init__(self, block_environment: BlocksEnvironment):
        super().__init__()
        self.block_environment = block_environment
        self.s_for_every_step = 1
        self.block_environment.cells[0][0][0].state.temperature = 1200
        self.block_environment.cells[0][0][0].next_state.temperature = 1200
        for x in range(self.block_environment.size[0]):
            for y in range(self.block_environment.size[1]):
                for z in range(self.block_environment.size[2]):
                    cell: Cell = self.block_environment.cells[x][y][z]
                    if cell.material_properties.is_gas():
                        cell.collider = None
        for x in range(self.block_environment.size[0]):
            for y in range(self.block_environment.size[1]):
                for z in range(self.block_environment.size[2]):
                    if self.block_environment.cells[x][y][z] is not None:
                        for i in [-1, 1]:
                            if 0 <= x + i < self.block_environment.size[0]:
                                self.block_environment.cells[x][y][z].add_neighbor(
                                    self.block_environment.cells[x + i][y][z])
                        for j in [-1, 1]:
                            if 0 <= y + j < self.block_environment.size[1]:
                                self.block_environment.cells[x][y][z].add_neighbor(
                                    self.block_environment.cells[x][y + j][z])
                        for k in [-1, 1]:
                            if 0 <= z + k < self.block_environment.size[2]:
                                self.block_environment.cells[x][y][z].add_neighbor(
                                    self.block_environment.cells[x][y][z + k])

                    cell: Cell = self.block_environment.cells[x][y][z]
                    cell.collider = None
                    if cell.voxel is not None:
                        cell.voxel.collider = None
                    if not cell.material_properties.is_gas():
                        print(x, y, z)
                        for x2 in [0, self.block_environment.size[0] - 1]:
                            for y2 in range(max(0, y - 5), min(self.block_environment.size[1], y + 5)):
                                for z2 in range(max(0, z - 5), min(self.block_environment.size[2], z + 5)):
                                    cell2: Cell = self.block_environment.cells[x2][y2][z2]
                                    self.dispatch_ray(cell, cell2)
                        for x2 in range(max(0, x - 5), min(self.block_environment.size[0], x + 5)):
                            for y2 in [0, self.block_environment.size[1] - 1]:
                                for z2 in range(max(0, z - 5), min(self.block_environment.size[2], z + 5)):
                                    cell2: Cell = self.block_environment.cells[x2][y2][z2]
                                    self.dispatch_ray(cell, cell2)
                        for x2 in range(max(0, x - 5), min(self.block_environment.size[0], x + 5)):
                            for y2 in range(max(0, y - 5), min(self.block_environment.size[1], y + 5)):
                                for z2 in [0, self.block_environment.size[2] - 1]:
                                    cell2: Cell = self.block_environment.cells[x2][y2][z2]
                                    self.dispatch_ray(cell, cell2)
                    cell.collider = BoxCollider(cell, center=Vec3(cell.position[0] + 0.5, cell.position[1] + 0.5,
                                                                  cell.position[2] + 0.5), size=Vec3(1, 1, 1))
                    if cell.voxel is not None:
                        cell.voxel.collider = BoxCollider(cell,
                                                          center=Vec3(cell.position[0] + 0.5, cell.position[1] + 0.5,
                                                                      cell.position[2] + 0.5), size=Vec3(1, 1, 1))

        with open('neighbours.txt', 'w') as f:
            original_stdout = sys.stdout
            sys.stdout = f  # Change the standard output to the file we created.
            for x in range(self.block_environment.size[0]):
                for y in range(self.block_environment.size[1]):
                    for z in range(self.block_environment.size[2]):
                        self.block_environment.cells[x][y][z].radiation_neighors = \
                        list(set(self.block_environment.cells[x][y][z].radiation_neighbors))
                        print("(", x, y, z, ")", list(set(self.block_environment.cells[x][y][z].radiation_neighbors)))
                        tmp_list = []
                        for pos in self.block_environment.cells[x][y][z].radiation_neighors:
                            tmp_list.append(self.block_environment.cells[pos[0]][pos[1]][pos[2]])
                        self.block_environment.cells[x][y][z].radiation_neighors = tmp_list
            sys.stdout = original_stdout



    def dispatch_ray(self, cell, cell2):
        hit_info = raycast(cell.position, cell2.position - cell.position, distance=5)
        if hit_info.hit:
            cell_hit: Cell = \
                self.block_environment.cells[int(hit_info.entity.position[0])][int(hit_info.entity.position[1])][
                    int(hit_info.entity.position[2])]
            if not cell_hit.material_properties.is_gas():
                cell_hit.radiation_neighbors.append(cell.position)
                cell.radiation_neighbors.append(cell_hit.position)

    def next_10(self):
        self.next_step(100)

    def next_step(self, n=1):
        for i in range(n):
            for x in range(self.block_environment.size[0]):
                for y in range(self.block_environment.size[1]):
                    for z in range(self.block_environment.size[2]):
                        if self.block_environment.cells[x][y][z] is not None:
                            cell: Cell = self.block_environment.cells[x][y][z]
                            cell.next_temps = [cell.state.temperature] * 6
            for x in range(self.block_environment.size[0]):
                for y in range(self.block_environment.size[1]):
                    for z in range(self.block_environment.size[2]):
                        if self.block_environment.cells[x][y][z] is not None:
                            self.block_environment.cells[x][y][z].calc_next_state(self.s_for_every_step)

            # print(self.block_environment.cells[0][0][0].state.temperature)
            # print(self.block_environment.cells[0][0][1].next_temps)
            # print(self.block_environment.cells[1][0][0].next_temps)
            # print(self.block_environment.cells[0][0][0].next_temps)
            for x in range(self.block_environment.size[0]):
                for y in range(self.block_environment.size[1]):
                    for z in range(self.block_environment.size[2]):
                        if self.block_environment.cells[x][y][z] is not None:
                            cell: Cell = self.block_environment.cells[x][y][z]
                            cell.state = copy(cell.next_state)
                            cell.state.temperature = sum(cell.next_temps) / 6

        self.block_environment.refresh_voxels()

    def run(self):
        while True:
            self.next_step(5)
