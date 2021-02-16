#!/usr/bin/env python3


import rospy
import os

from transitions import Machine
import time
import csv

from state_machine.msg import Behav_mov

class Robot(object):

    states = ['ligar', 'crise_existencial', 'procurar_por_manteiga', 'buscar_manteiga', 'passar_manteiga']

    def __init__(self, name):

        # Define o nome do seu robô que passa manteiga!
        self.name = name

        #Define um Publisher (ROS)
        self.pubMov = rospy.Publisher('behaviour_movimento', Behav_mov, queue_size=100)

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

    def readCsv(self):
        file = open('data.csv', 'r')
        data = csv.reader(file)
        for line in data:
            if(line[0] == 'x_centro'):
                self.x_centro = int(line[1])
            if(line[0] == 'y_centro'):
                self.y_centro = int(line[1])
            if(line[0] == 'roi_largura'):
                self.roi_largura = int(line[1])
            if(line[0] == 'roi_altura'):
                self.roi_altura = int(line[1])
            if(line[0] == 'manteiga_encontrada'):
                self.manteiga_encontrada = bool(line[1] == 'True')
        file.close()
    
    #!PUBLISHER AND SUBSCRIBER
    def publishToMov(self):
        msg_mov = Behav_mov()
        msg_mov.move = self.movimento
        self.pubMov.publish(msg_mov)

    #!MÉTODOS MOVIMENTO 
    def move_forward(self):
        #*Movimento para o robô se deslocar para frente
        self.movimento = 1
        print('Robô se movimento para frente\n')

    def walk_back(self):
        #*Movimento para o robô se deslocar para trás
        self.movimento = 2
        print('Robô se movimentando para trás\n')

    def rotate_time(self):
        #*Movimento para o robô rotacionar em sentido horário
        self.movimento = 3
        print('Robô rotacionando no sentido horário\n')

    def rotate_counterclockwise(self):
        #*Movimento para o robô rotacionar em sentido anti-horário
        self.movimento = 4
        print('Robô rotacionando no sentido anti-horário\n')
    
    def butter(self):
        #*Movimento para o robô "passar manteiga"
        self.movimento = 5
        print('Robô passando manteiga\n')

    #!MÉTODOS - VISÃO
    def connect_neural_network(self):
        #*Ligar a rede neural
        print('Ligando rede neural\n')

    def turn_off_neural_network(self):
        #*Desligar a rede neural
        print('Desligando rede neural\n')

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
    
    rospy.init_node('state_node', anonymous=True)
    #rospy.spin()
    robot = Robot('passador de manteiga')

    while not rospy.is_shutdown():
        robot.publishToMov()
        robot.readCsv()
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
            alignment = robot.alignment()
            if(alignment == 'direita'):
                robot.rotate_time() #Chamando método que rotaciona a robô sentido horário
            elif(alignment == 'esquerda'):
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