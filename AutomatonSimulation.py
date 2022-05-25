from BlocksEnvironment import BlocksEnvironment


class AutomatonSimulation:
    def __init__(self, block_environment: BlocksEnvironment):
        self.block_environment = block_environment
        #TODO: add neighbours here

    def next_step(self):
        for x in range(self.block_environment.size[0]):
            for y in range(self.block_environment.size[1]):
                for z in range(self.block_environment.size[2]):
                    self.block_environment.cells[x][y][z].calc_next_state()

        for x in range(self.block_environment.size[0]):
            for y in range(self.block_environment.size[1]):
                for z in range(self.block_environment.size[2]):
                    self.block_environment.cells[x][y][z].state = self.block_environment.cells[x][y][z].next_state
