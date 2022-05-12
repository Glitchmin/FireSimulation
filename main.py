from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()
window.title = 'My Game'  # The window title
window.borderless = False  # Show a border
window.fullscreen = False  # Do not go Fullscreen
window.exit_button.visible = False  # Do not show the in-game red X that loses the window
window.fps_counter.enabled = True  # Show the FPS (Frames per second) counter


class Voxel(Button):
    def __init__(self, position=(0, 0, 0)):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            origin_y=.5,
            texture='white_cube',
            color=color.color(0, 0, random.uniform(.9, 1.0)),
            highlight_color=color.lime,
        )

    # def input(self, key):
    #     if self.hovered:
    #         if key == 'left mouse down':
    #             voxel = Voxel(position=self.position + mouse.normal)
    #
    #         if key == 'right mouse down':
    #             destroy(self)


for z in range(8):
    for x in range(8):
        voxel = Voxel(position=(x, 0, z))

if __name__ == "__main__":

    # def update():

    def input(key):
        # if mouse.world_point:
        #     print(mouse.world_point)
        #     print(camera.world_position)
        #     print(camera.forward)
        if key == 'left mouse down':
            if mouse.world_point is not None:
                hit_info = raycast(camera.world_position, mouse.world_point - camera.world_position, distance=inf)
                if hit_info.hit:
                    Voxel(position=hit_info.entity.position + hit_info.normal)


    player = EditorCamera()
    app.run()
