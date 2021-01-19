# coding=utf-8

import rospy
from transitions import Machine
import os
import time

class Robot(object):

    states = ['ligar', 'crise_existencial', 'procurar_por_manteiga', 'buscar_manteiga', 'passar_manteiga']

    def __init__(self, name):

        # Define o nome do seu robô que passa manteiga!
        self.name = name

        #Define vairáveis que serão utilizadas
        self.x_centro = 0
        self.y_centro = 0
        self.roi_largura = 0
        self.roi_altura = 0
        self.manteiga_encontrada = False
        self.rede_neural_ligada = False
        self.movimento = -1

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
        count = 1
        #*Método que conterá toda a lógica do robô
        os.system('clear') #Limpando o terminal
        print('Iniciando behaviour...\n')
        self.connect_neural_network() #Chamando método que liga a rede neural
        while True:
            time.sleep(2)
            if(count == 2):
                self.manteiga_encontrada = True
                print('Manteiga encontrada\n')
            count = count +1
            if(self.manteiga_encontrada):
                alignment = self.alignment() #Chamando método que retorna alinhamento da manteiga
                if(alignment == 'direita'):
                    self.rotate_time() #Chamando método que rotaciona a robô sentido horário
                elif(alignment == 'esquerda'):
                    self.rotate_counterclockwise() #Chamando método que rotaciona a robô sentido anti-horário
                else:
                    if(self.close_enough()):
                        self.butter() #Chamando método que busca o movimento de passar manteiga
                        self.turn_off_neural_network() #Chamando método que desliga a rede neural
                        break
                    else:
                        self.move_forward() #Chamando método que se movimenta para frente
                        pass
            else:
                print('Procurando manteiga..\n')
                self.rotate_time() #Chamando método que rotaciona a robô sentido horário
        

    #!MÉTODOS MOVIMENTO 
    def move_forward(self):
        #*Movimento para o robô se deslocar para frente
        #CÓDIGO DO MOVIMENTO: 1
        self.roi_largura = self.roi_largura + 1 
        print('Robô se movimento para frente\n')

    def walk_back(self):
        #*Movimento para o robô se deslocar para trás
        #CÓDIGO DO MOVIMENTO: 2
        self.roi_largura = self.roi_largura - 1 
        print('Robô se movimentando para trás\n')

    def rotate_time(self):
        #*Movimento para o robô rotacionar em sentido horário
        #CÓDIGO DO MOVIMENTO: 3
        self.x_centro = self.x_centro - 1
        print('Robô rotacionando no sentido horário\n')

    def rotate_counterclockwise(self):
        #*Movimento para o robô rotacionar em sentido anti-horário
        #CÓDIGO DO MOVIMENTO: 4
        self.x_centro = self.x_centro + 1
        print('Robô rotacionando no sentido anti-horário\n')
    
    def butter(self):
        #*Movimento para o robô "passar manteiga"
        #CÓDIGO DO MOVIMENTO: 5
        print('Robô passando manteiga\n')

    #!MÉTODOS - VISÃO
    def connect_neural_network(self):
        #*Ligar a rede neural
        print('Ligando rede neural\n')
        self.rede_neural_ligada = True

    def turn_off_neural_network(self):
        #*Desligar a rede neural
        print('Desligando rede neural\n')
        self.rede_neural_ligada = False

    def alignment(self):
        #*Confere o alinhamento da manteiga em ralação ao centro da robô
        if(self.x_centro > 0):
            print('Alinhamento da manteiga para direita\n')
            return 'direita'
        elif(self.x_centro < 0):
            print('Alinhamento da manteiga para esquerda\n')
            return 'esquerda'
        else:
            print('Alinhamento da manteiga centralizado\n')
            return 'centro'
        

    
    def close_enough(self):
        #*Confere se a manteiga está perto o suficiente
        if(self.roi_largura > 5):
            print('Manteiga perto o suficiente\n')
            return True
        else:
            print('Manteiga não está perto o suficiente\n')
            return False


robot = Robot('passador de manteiga')
robot.start()
