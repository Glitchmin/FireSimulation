import threading
from copy import copy

from BlocksEnvironment import BlocksEnvironment
from Cell import Cell
from constants import BLOCK_SIZE_M


class AutomatonSimulation(threading.Thread):
    def __init__(self, block_environment: BlocksEnvironment):
        super().__init__()
        self.block_environment = block_environment
        self.s_for_every_step = 1
        self.block_environment.cells[7][0][7].state.temperature = 1200
        self.block_environment.cells[7][0][7].next_state.temperature = 1200
        # self.block_environment.cells[3][0][2].state.temperature = 1200
        # self.block_environment.cells[3][0][2].next_state.temperature = 1200
        # for x in range(self.block_environment.size[0]):
        #     for z in range(self.block_environment.size[2]):
        #         if 0 < x < self.block_environment.size[0]-1 and 0 < z < self.block_environment.size[2]-1:
        #             self.block_environment.cells[x][0][z].next_state.temperature = 273 + 250+10
        #             self.block_environment.cells[x][0][z].state.temperature = 273 + 250+10
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
                        self.block_environment.cells[x][y][z].calc_rad_fact()
                        # print(x, y, z, self.block_environment.cells[x][y][z].radiation_factor)

    def next_10(self):
        self.next_step(100)

    def next_step(self, n=1):
        for i in range(n):
            Cell.radiation_sum = 0
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
                            self.block_environment.cells[x][y][z].calculate_radiation_heat(self.s_for_every_step)

            for x in range(self.block_environment.size[0]):
                for y in range(self.block_environment.size[1]):
                    for z in range(self.block_environment.size[2]):
                        if self.block_environment.cells[x][y][z] is not None:
                            self.block_environment.cells[x][y][z].calc_next_state(self.s_for_every_step)

            # print(self.block_environment.cells[0][0][0].state.temperature)
            # print(self.block_environment.cells[0][0][1].next_temps)
            # print(self.block_environment.cells[1][0][0].next_temps)
            # print(self.block_environment.cells[0][0][0].next_temps)
            smoke_sum = 0
            prev_smoke_sum = 0
            prev_heat_sum = 0
            heat_sum = 0
            theoretical_heat_generation = 0
            for x in range(self.block_environment.size[0]):
                for y in range(self.block_environment.size[1]):
                    for z in range(self.block_environment.size[2]):
                        if self.block_environment.cells[x][y][z] is not None:
                            cell: Cell = self.block_environment.cells[x][y][z]
                            prev_smoke_sum += cell.state.smoke_saturation
                            prev_heat_sum += cell.state.temperature * cell.material_properties.specific_heat * cell.material_properties.density * BLOCK_SIZE_M**3
                            cell.state = copy(cell.next_state)
                            cell.state.temperature = sum(cell.next_temps) / 6
                            smoke_sum += cell.state.smoke_saturation
                            heat_sum += cell.state.temperature * cell.material_properties.specific_heat * cell.material_properties.density * BLOCK_SIZE_M**3
                            if cell.state.is_burning:
                                theoretical_heat_generation += cell.material_properties.heat_generation_s * self.s_for_every_step


            # print(f"smoke sum: {smoke_sum}, diff: {smoke_sum-prev_smoke_sum}")
            print(f"heat sum: {heat_sum}, diff: {heat_sum-prev_heat_sum}, theoretical: {theoretical_heat_generation}")
        self.block_environment.refresh_voxels()

    def run(self):
        while True:
            self.next_step(4)
