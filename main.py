from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

from AutomatonSimulation import AutomatonSimulation
from BlocksEnvironment import BlocksEnvironment

app = Ursina()
window.title = 'Burn baby burn!'
window.borderless = False
# window.fullscreen = True
window.exit_button.visible = True
window.fps_counter.enabled = True
env = BlocksEnvironment(15, 15, 15)
sim = None
sim_button = None
sim_tooltip = None

def start_sim():
    global sim, sim_button
    sim.start()
    # sim_button.text = 'next step'
    # sim_button.on_click = sim.next_step
    #

if __name__ == "__main__":
    # def update():

    sim = AutomatonSimulation(env)
    b = Button(text='view \nmode', color=color.azure, scale=.1, text_origin=(-.5, 0),
               position=window.bottom_left + (0.07, 0.07))
    b.on_click = env.switch_view_mode

    sim_button = Button(text='start \nsimulation', color=color.azure, scale=(0.18, 0.1), text_origin=(-.5, 0),
                        position=window.bottom_left + (0.3, 0.07))
    sim_button.on_click = start_sim

    next_button = Button(text='next 10', color=color.azure, scale=(0.18, 0.1), text_origin=(-.5, 0),
                        position=window.bottom_left + (0.5, 0.07))
    next_button.on_click = sim.next_step


    player = EditorCamera()
    # player = FirstPersonController()
    app.run()
