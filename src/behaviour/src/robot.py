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

def main():
    robot = Robot('passador de manteiga')
    count = 1
    while True:
        
        if(count < 3):
            robot.manteiga_encontrada = True

        time.sleep(2)
        if(robot.state == 'ligar'):
            os.system('clear') #Limpando o terminal
            print('------ESTADO ATUAL:' + robot.state + '------\n\n')
            print('Iniciando behaviour...\n')
            robot.connect_neural_network() #Chamando método que liga a rede neural
            robot.wake_up()

        elif(robot.state == 'crise_existencial'):
            os.system('clear') #Limpando o terminal
            print('------ESTADO ATUAL:' + robot.state + '------\n\n')
            print('Tendo uma crise existencial!\n')
            robot.where_butter()

        elif(robot.state == 'procurar_por_manteiga'):
            os.system('clear') #Limpando o terminal
            print('------ESTADO ATUAL:' + robot.state + '------\n\n')
            print('Procurando manteiga..\n')
            robot.rotate_time() #Chamando método que rotaciona a robô sentido horário
            if(robot.manteiga_encontrada):
                robot.seeking_the_butter()

        elif(robot.state == 'buscar_manteiga'):
            os.system('clear') #Limpando o terminal
            print('------ESTADO ATUAL:' + robot.state + '------\n\n')
            if(robot.alignment == 'direita'):
                robot.rotate_time() #Chamando método que rotaciona a robô sentido horário
            elif(robot.alignment == 'esquerda'):
                robot.rotate_counterclockwise() #Chamando método que rotaciona a robô sentido anti-horário
            else:
                if(robot.close_enough()):
                    robot.buterry()
                else:
                    robot.move_forward()

        elif(robot.state == 'passar_manteiga'):
            os.system('clear') #Limpando o terminal
            print('------ESTADO ATUAL:' + robot.state + '------\n\n')
            robot.butter() #Chamando método que busca o movimento de passar manteiga
            robot.turn_off_neural_network() #Chamando método que desliga a rede neural
            break
        
        else:
            break

main()