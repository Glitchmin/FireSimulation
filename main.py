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
    sim = AutomatonSimulation(env)
    sim_button.text = 'next step'
    sim_button.on_click = sim.next_step
    sim_tooltip = Tooltip('calculate next step of the simulation')
    sim_button.tooltip = sim_tooltip


if __name__ == "__main__":
    # def update():

    b = Button(text='view \nmode', color=color.azure, scale=.1, text_origin=(-.5, 0),
               position=window.bottom_left + (0.1, 0.1))
    b.on_click = env.switch_view_mode
    b.tooltip = Tooltip('toggle thermal')

    sim_button = Button(text='start \nsimulation', color=color.azure, scale=.1, text_origin=(-.5, 0),
                        position=window.bottom_left + (1.1, 0.1))
    sim_button.on_click = start_sim
    sim_tooltip = Tooltip('start the simulation')
    sim_button.tooltip = sim_tooltip

    player = EditorCamera()
    # player = FirstPersonController()
    app.run()
