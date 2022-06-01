from copy import copy

from BlocksEnvironment import BlocksEnvironment


class AutomatonSimulation:
    def __init__(self, block_environment: BlocksEnvironment):
        self.block_environment = block_environment
        self.s_for_every_step = 5e-2
        self.block_environment.cells[0][0][0].state.temperature = 1200
        self.block_environment.cells[0][0][0].next_state.temperature = 1200
        self.block_environment.cells[0][0][3].state.temperature = 1200
        self.block_environment.cells[0][0][3].next_state.temperature = 1200
        self.block_environment.cells[5][0][5].state.temperature = 1700
        self.block_environment.cells[5][0][5].next_state.temperature = 1700
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

    def next_step(self, steps=50):
        if steps == 0:
            return
        total_heat = 0
        for x in range(self.block_environment.size[0]):
            for y in range(self.block_environment.size[1]):
                for z in range(self.block_environment.size[2]):
                    if self.block_environment.cells[x][y][z] is not None:
                        self.block_environment.cells[x][y][z].calc_next_state(self.s_for_every_step)
                        total_heat += self.block_environment.cells[x][y][z].state.temperature *  self.block_environment.cells[x][y][z].material_properties.specific_heat *  self.block_environment.cells[x][y][z].material_properties.density
        print("total heat:", total_heat)

        for x in range(self.block_environment.size[0]):
            for y in range(self.block_environment.size[1]):
                for z in range(self.block_environment.size[2]):
                    if self.block_environment.cells[x][y][z] is not None:
                        self.block_environment.cells[x][y][z].state = copy(self.block_environment.cells[x][y][z].next_state)
        self.block_environment.refresh_voxels()

        self.next_step(steps-1)
