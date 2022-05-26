from BlocksEnvironment import BlocksEnvironment


class AutomatonSimulation:
    def __init__(self, block_environment: BlocksEnvironment):
        self.block_environment = block_environment
        self.ms_for_every_step = 100
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
                        self.block_environment.cells[x][y][z].calc_next_state(self.ms_for_every_step)

        for x in range(self.block_environment.size[0]):
            for y in range(self.block_environment.size[1]):
                for z in range(self.block_environment.size[2]):
                    if self.block_environment.cells[x][y][z] is not None:
                        self.block_environment.cells[x][y][z].state = self.block_environment.cells[x][y][z].next_state
