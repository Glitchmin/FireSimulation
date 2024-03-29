from ursina import *
from MaterialProperties import MaterialProperties
from StateProperties import StateProperties
from ColorToTemperature import ColorToTemperature
from constants import BLOCK_SIZE_M, CONVECTION_VERTICAL_RATIO, CONVECTION_HORIZONTAL_RATIO, ROOM_TEMPERATURE, \
    RADIATION_CONSTANT, FLAME_MIN_TEMP


class Voxel(Button):
    fire_color = color.color(0, 0.8, 1)
    flame_color = color.color(0, 0.8, 1, 0.5)

    def __init__(self, position, color_hsv):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            origin_y=.5,
            texture='white_cube',
            color=color.color(*color_hsv),
            # color=color.rgb(*ColorToTemperature().convert_K_to_RGB(290)),
            highlight_color=color.color(color_hsv[0], min(1, color_hsv[1] * 1.3), 1),
        )


class Cell(Entity):
    radiation_sum = 0
    rad_walls_sum = 0

    def __init__(self, position, material_properties: MaterialProperties, state: StateProperties, **kwargs):
        super().__init__(**kwargs)
        self.material_properties = material_properties
        self.state = state
        self.next_state = copy(state)
        self.next_temps = [state.temperature] * 6
        self.neighbors: [Cell] = []
        self.voxel = None
        self.position = position
        self.radiation_factor = 0
        if not self.material_properties.is_invisible():
            self.voxel = Voxel(position, material_properties.color)

    def to_string(self):
        return str(self.material_properties.id)

    def input(self, key):
        if key == 'g':
            self.voxel.color = color.rgb(*ColorToTemperature().convert_K_to_RGB(self.state.temperature))

    def update_voxel(self, thermal_mode):
        if thermal_mode:
            if not self.material_properties.is_invisible():
                self.voxel.color = color.rgb(*ColorToTemperature().convert_K_to_RGB(self.state.temperature))
            elif abs(self.state.temperature - ROOM_TEMPERATURE) > 20:
                if self.voxel is None:
                    self.voxel = Voxel(self.position, color.color(1, 1, 1, 1))
                self.voxel.color = color.rgba(*ColorToTemperature().convert_K_to_RGB(self.state.temperature), 255 * 0.5)
            else:
                if self.voxel is not None:
                    destroy(self.voxel)
        else:
            smoke_saturation = min(max(0., self.state.smoke_saturation), 1.)
            if self.state.is_burning:
                if self.voxel is None:
                    self.voxel = Voxel(self.position, self.material_properties.color)
                if self.material_properties.is_transparent():
                    self.voxel.color = Voxel.flame_color
                else:
                    self.voxel.color = Voxel.fire_color
            elif not self.material_properties.is_invisible():
                self.voxel.color = color.color(*self.material_properties.color)
            elif smoke_saturation > 0.005 or self.state.smoke_saturation < 0:
                saturation = 0.6 if self.state.temperature > FLAME_MIN_TEMP else 0
                alpha_mul = 2. if self.state.temperature > FLAME_MIN_TEMP else 1.
                if self.voxel is None:
                    self.voxel = Voxel(self.position, self.material_properties.color)
                if self.state.smoke_saturation < 0:
                    self.voxel.color = color.color(200, 1, 1)
                elif self.state.smoke_saturation > 1:

                    self.voxel.color = color.color(0, saturation, min(1., alpha_mul*0.6))
                else:
                    self.voxel.color = color.color(0, saturation, min(1., alpha_mul*0.5), min(1., alpha_mul*self.state.smoke_saturation))
            elif self.voxel is not None:
                destroy(self.voxel)

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

    def calc_rad_fact(self):
        if self.material_properties.is_gas():
            return

        for neighbor in self.neighbors:
            if neighbor.material_properties.is_gas():
                self.radiation_factor += 1
                Cell.rad_walls_sum += 1

    def calc_next_state(self, time_s):
        self.calculate_is_burning()

        self.calculate_radiation()
        self.calculate_conduction(time_s)
        self.calculate_convection(time_s)
        self.calculate_smoke(time_s)
        self.calculate_fire(time_s)

    def calculate_is_burning(self):
        flash_active = self.state.is_burning
        for neighbor in self.neighbors:
            if neighbor.state.is_burning:
                flash_active = True

        if flash_active:
            self.next_state.is_burning = self.state.temperature >= self.material_properties.flash_temp
        else:
            self.next_state.is_burning = self.state.temperature >= self.material_properties.autoignition_temp

    def calculate_fire(self, time_s):
        if self.state.is_burning:
            for i in range(6):
                self.next_temps[i] += self.material_properties.heat_generation_s * time_s / (
                            self.material_properties.specific_heat *
                            self.material_properties.density * BLOCK_SIZE_M ** 3)
        else:
            igniters_counters = 0
            for neighbor in self.neighbors:
                if neighbor.state.temperature > self.material_properties.flash_temp and neighbor.state.is_burning:
                    igniters_counters += 1

            for i in range(6):
                self.next_temps[i] += igniters_counters / 6 * self.material_properties.heat_generation_s * time_s / (
                        self.material_properties.specific_heat *
                        self.material_properties.density * BLOCK_SIZE_M ** 3)

    def calculate_smoke(self, time_s):
        if not self.material_properties.is_gas():
            if self.state.is_burning:
                for neighbor in self.neighbors:
                    if neighbor is not None and neighbor.material_properties.is_gas() and\
                            neighbor.position[1] > self.position[1]:
                        neighbor.next_state.smoke_saturation += self.material_properties.smoke_generation_s * time_s
            return

        is_ceiling_above = True
        for neighbor in self.neighbors:
            # if self.position == (0, 2, 0) and neighbor is not None:
            # if neighbor is not None and neighbor.position[1] > self.position[1] \
            #         and not neighbor.material_properties.is_gas():
                # print(">>>", neighbor.material_properties.is_gas(), neighbor.material_properties.id, self.position, "neigh: ", neighbor.position)

            if neighbor is not None and neighbor.position[1] > self.position[1] \
                    and neighbor.material_properties.is_gas():
                is_ceiling_above = False

        intermediate_smoke = self.state.smoke_saturation

        equal_y_neighbors = 0
        neighbor_smoke_space = 0.
        neighbor_down_space = 0.
        neighbor_up_space = 0.

        for neighbor in self.neighbors:
            if neighbor is not None:
                if neighbor.position[1] == self.position[1]:
                    equal_y_neighbors += 1
                    neighbor_smoke_space += max(0., 1.-neighbor.state.smoke_saturation)
                elif neighbor.position[1] < self.position[1]:
                    neighbor_down_space = max(0., 1.-neighbor.state.smoke_saturation)
                elif neighbor.position[1] > self.position[1]:
                    neighbor_up_space = max(0., 1.-neighbor.state.smoke_saturation)

        for neighbor in self.neighbors:
            if neighbor.position[1] > self.position[1]:
                if self.state.smoke_saturation != 0 and neighbor.state.smoke_saturation < 1:
                    smoke_up = 0.8 * intermediate_smoke
                    neighbor.next_state.smoke_saturation += smoke_up
                    intermediate_smoke -= smoke_up
            elif neighbor.position[1] < self.position[1]:
                if intermediate_smoke >= 1.0:
                    initial_down_smoke = min(neighbor_down_space, (intermediate_smoke - 1.0)*3/4)
                    # propagated_sideways_smoke = min(neighbor_smoke_space, initial_down_smoke)
                    # propagated_down_smoke = intermediate_smoke-1. - propagated_sideways_smoke
                    # propagated_down_smoke = (intermediate_smoke - 1.0)/2
                    propagated_down_smoke = initial_down_smoke
                    neighbor.next_state.smoke_saturation += propagated_down_smoke
                    intermediate_smoke -= propagated_down_smoke

        # pre_neighbor_split_smoke = max(0., intermediate_smoke-1.)
        # intermediate_smoke = self.divide_to_neigbours(equal_y_neighbors, intermediate_smoke, pre_neighbor_split_smoke)

        pre_neighbor_split_smoke = intermediate_smoke
        divider = 50
        if intermediate_smoke > 0.3:
            divider = 14
        if is_ceiling_above or neighbor_up_space < 0.1:
            # print("is_ceiling_above or neighbor_up_space < 0.1", self.position)
            # divider = 6*equal_y_neighbors/4
            divider = 6
        # if not is_ceiling_above and neighbor_up_space < 0.9:
        #     divider = 6/(1-neighbor_up_space)
        # if pre_neighbor_split_smoke > 1 and pre_neighbor_split_smoke/divider*equal_y_neighbors > 0.9:
        #     print("side propagated over excess smoke:", pre_neighbor_split_smoke, pre_neighbor_split_smoke/divider*equal_y_neighbors)
        intermediate_smoke = self.divide_to_neighbors(divider, intermediate_smoke, pre_neighbor_split_smoke)

        self.next_state.smoke_saturation += (intermediate_smoke - self.state.smoke_saturation)
        # if intermediate_smoke != 0:
        #     print(f"state {self.state.smoke_saturation}, inter: {intermediate_smoke}, next {self.next_state.smoke_saturation}")

    def divide_to_neighbors(self, divider, intermediate_smoke, pre_neighbor_split_smoke):
        for neighbor in self.neighbors:
            if neighbor is not None:
                if neighbor.position[1] == self.position[1]:
                    neighbor.next_state.smoke_saturation += pre_neighbor_split_smoke / divider
                    intermediate_smoke -= pre_neighbor_split_smoke / divider
        return intermediate_smoke

    def get_neigh_num(self, neighbor):
        if self.position.x - neighbor.position.x > 0:
            return 0
        if self.position.x - neighbor.position.x < 0:
            return 1
        if self.position.y - neighbor.position.y > 0:
            return 2
        if self.position.y - neighbor.position.y < 0:
            return 3
        if self.position.z - neighbor.position.z > 0:
            return 4
        if self.position.z - neighbor.position.z < 0:
            return 5

    def calculate_conduction(self, time_s):
        for neighbor in self.neighbors:
            num = self.get_neigh_num(neighbor)
            if neighbor is not None:
                R1 = BLOCK_SIZE_M / 2 / self.material_properties.conductivity
                R2 = BLOCK_SIZE_M / 2 / neighbor.material_properties.conductivity
                R = R1 + R2
                U = 1 / R
                q = U * BLOCK_SIZE_M * BLOCK_SIZE_M / 6 * (neighbor.state.temperature - self.state.temperature)
                control_const = 1 + 999*(not neighbor.material_properties.is_gas() and not self.material_properties.is_gas())
                heat = control_const * q * time_s
                sign = -1 if heat < 0 else (1 if heat > 0 else 0)
                heat = sign * min(abs(heat), max(neighbor.state_heat(), self.state_heat(), 0))
                if self.state.temperature > neighbor.state.temperature and heat > 0:
                    print()
                    print("WRONG TEMP CONDUCTION DIRECTION")
                    print()
                self.next_temps[num] += heat / (self.material_properties.specific_heat *
                                                self.material_properties.density * BLOCK_SIZE_M ** 3)

    def state_heat(self):
        return self.state.temperature * self.material_properties.specific_heat *\
               self.material_properties.density * BLOCK_SIZE_M**3

    def calculate_convection(self, time_s):
        if not self.material_properties.is_gas():
            return

        for neighbor in self.neighbors:
            num = self.get_neigh_num(neighbor)
            if neighbor is not None and neighbor.material_properties.is_gas():
                ratio = 0
                if self.position.y < neighbor.position.y:
                    ratio = CONVECTION_VERTICAL_RATIO
                if self.position.y == neighbor.position.y:
                    ratio = CONVECTION_HORIZONTAL_RATIO

                q = ratio * BLOCK_SIZE_M * BLOCK_SIZE_M * (self.state.temperature - neighbor.state.temperature)
                heat = q * time_s

                sign = -1 if heat < 0 else (1 if heat > 0 else 0)
                heat = sign * min(abs(heat), max(self.state_heat(), 0))
                neighbor.next_temps[num] += heat / (6 * neighbor.material_properties.specific_heat *
                                                    neighbor.material_properties.density * BLOCK_SIZE_M ** 3)
                self.next_temps[num] -= heat / (6 * self.material_properties.specific_heat *
                                                self.material_properties.density * BLOCK_SIZE_M ** 3)

    def calculate_radiation_heat(self, time_s):
        if self.material_properties.is_gas() and not self.state.is_burning:
            return

        q = RADIATION_CONSTANT * self.material_properties.emissivity * self.radiation_factor * pow(BLOCK_SIZE_M, 2) \
            * pow(self.state.temperature, 4)
        heat = q * time_s
        for i in range(6):
            self.next_temps[i] -= heat / (self.material_properties.specific_heat *
                                          self.material_properties.density * BLOCK_SIZE_M ** 3)

        Cell.radiation_sum += heat

    def calculate_radiation(self):
        heat = Cell.radiation_sum / Cell.rad_walls_sum
        heat *= self.radiation_factor
        for i in range(6):
            self.next_temps[i] += heat / (self.material_properties.specific_heat *
                                          self.material_properties.density * BLOCK_SIZE_M ** 3)
