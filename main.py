from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

from BlocksEnvironment import BlocksEnvironment

app = Ursina()
window.title = 'My Game'  # The window title
window.borderless = False  # Show a border
window.fullscreen = False  # Do not go Fullscreen
window.exit_button.visible = True  # Do not show the in-game red X that loses the window
window.fps_counter.enabled = True  # Show the FPS (Frames per second) counter

if __name__ == "__main__":
    # def update():

    env = BlocksEnvironment(8, 10, 5)

    player = EditorCamera()
    app.run()
