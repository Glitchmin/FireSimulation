from copy import copy

from BlocksEnvironment import BlocksEnvironment
from Cell import Cell


class AutomatonSimulation:
    def __init__(self, block_environment: BlocksEnvironment):
        self.block_environment = block_environment
        self.s_for_every_step = 10
        self.block_environment.cells[0][0][0].state.temperature = 1200
        self.block_environment.cells[0][0][0].next_state.temperature = 1200
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

    def next_step(self):
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

        print(self.block_environment.cells[0][0][0].state.temperature)
        print(self.block_environment.cells[0][0][1].next_temps)
        print(self.block_environment.cells[1][0][0].next_temps)
        print(self.block_environment.cells[0][0][0].next_temps)
        for x in range(self.block_environment.size[0]):
            for y in range(self.block_environment.size[1]):
                for z in range(self.block_environment.size[2]):
                    if self.block_environment.cells[x][y][z] is not None:
                        cell: Cell = self.block_environment.cells[x][y][z]
                        cell.state = copy(cell.next_state)
                        cell.state.temperature = sum(cell.next_temps) / 6
        self.block_environment.refresh_voxels()
