from transitions import Machine
import random

class Robot(object):

    states = ['ligar', 'crise_existencial', 'procurar_por_manteiga', 'buscar_manteiga', 'passar_manteiga']

    def __init__(self, name):

        # Define o nome do seu robô que passa manteiga!
        self.name = name

        # Iniciliza a maquina de estados
        self.machine = Machine(model=self, states=Robot.states, initial='ligar')

        # Toda manha ao acordar nosso robô irá ter uma crise existencial
        self.machine.add_transition(trigger='wake_up', source='ligar', dest='crise_existencial')

        # Após finalizar a crise existencial, ele deve procurar pela manteiga
        self.machine.add_transition(trigger='where_butter', source='crise_existencial', dest='procurar_por_manteiga')

        # Após saber a localização da manteiga, ele deve chegar até a manteiga
        self.machine.add_transition(trigger='seeking_the_butter', source='procurar_por_manteiga', dest='buscar_manteiga')

        # Agora que o robô já está na manteiga, vamos pega-la
        self.machine.add_transition(trigger='buterry', source='buscar_manteiga', dest='passar_manteiga')

    def start(self):
        robot.wake_up()
        while not rospy.is_shutdown():
            #LIGAR REDE NEURAL
            #SE TIVER ENCONTRADO MANTEIGA
                #ROTACIONA ATÉ CENTRALIZAR A MENTEIGA NO CENTRO
                #SE DESLOCA ATÉ A MANTEIGA UMA QUANTIDADE FIXA, E CONFERE SE JÁ ESTÁ PERTO O SUFICIENTE
                    #SE ESTIVER PERTO
                        #PASSA MANTEIGA
                    #SE NÃO ESTIVER PERTO
                        #VOLTA E ANDA A QUANTIDADE FIXA DNV E CONFERE DNV SE JÁ ESTÁ PERTO O SUFICIENTE
            #SE NÃO TIVER ENCONTRADO MANTEIGA 
                #ROTACIONA PARA CONTINUAR PROCURANDO




if __name__ == '__main__':
    passador_de_manteiga = Robot('Passador de Manteiga') #Inicia o construtor da classe
    passador_de_manteiga.start() #Roda o método start



