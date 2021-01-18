from transitions import Machine
import random

class Robot(object):

    states = ['turning_on', 'existential_crisis', 'look_for_butter', 'fetch_butter', 'get_butter']

    def __init__(self, name):

        # Define o nome do seu robô que passa manteiga!
        self.name = name

        # Iniciliza a maquina de estados
        self.machine = Machine(model=self, states=Robot.states, initial='turning_on')

        # Toda manha ao acordar nosso robô irá ter uma crise existencial
        self.machine.add_transition(trigger='wake_up', source='turning_on', dest='existential_crisis')

        # Após finalizar a crise existencial, ele deve procurar pela manteiga
        self.machine.add_transition(trigger='where_butter', source='existential_crisis', dest='look_for_butter')

        # Após saber a localização da manteiga, ele deve chegar até a manteiga
        self.machine.add_transition(trigger='seeking_the_butter', source='look_for_butter', dest='fetch_butter')

        # Agora que o robô já está na manteiga, vamos pega-la
        self.machine.add_transition(trigger='buterry', source='fetch_butter', dest='get_butter')

robot = Robot("Budega")
robot.wake_up()
print(robot.state)
robot.where_butter()
print(robot.state)


