from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

from BlocksEnvironment import BlocksEnvironment

app = Ursina()
window.title = 'Burn baby burn!'
window.borderless = False
# window.fullscreen = True
window.exit_button.visible = True
window.fps_counter.enabled = True

if __name__ == "__main__":
    # def update():

    env = BlocksEnvironment(15, 15, 15)

    b = Button(text='view mode', color=color.azure, scale=.1, text_origin=(-.5, 0), position=window.bottom_left+(0.1, 0.1))
    b.on_click = env.switch_view_mode
    b.tooltip = Tooltip('toggle thermal')

    player = EditorCamera()
    #player = FirstPersonController()
    app.run()
