#!/usr/bin/env python3

import rospy
import os

from transitions import Machine
import time

from state_machine.msg import Behav_mov
from state_machine.msg import Behav_vis
from butter_detection.msg import visparabeh

class Robot(object):

    states = ['ligar', 'crise_existencial', 'procurar_manteiga', 'buscar_manteiga', 'passar_manteiga', 'desligar']

    def __init__(self, name):

        #Nome do robo que passa manteiga
        self.name = name

        #Criando o Subscriber(ROS)
        self.subToVis = rospy.Subscriber('visao_behaviour', visparabeh, self.visionCallback)

        #Criando os Publishers(ROS)
        self.pubMov = rospy.Publisher('behaviour_movimento', Behav_mov, queue_size = 100)
        self.pubVis = rospy.Publisher('behaviour_visao', Behav_vis, queue_size = 100)

        #Definir as variaveis
        self.x_centro = 0
        self.y_centro = 0
        self.roi_largura = 0
        self.roi_altura = 0
        self.manteiga_encontrada = False
        self.rede_neural_ligada = False
        self.movimento = 'init_position'

        #Inicilizando maquina de estados
        self.machine = Machine(model = self, states = Robot.states, initial = 'ligar')

        #Robo acordou e teve um mini crise existencial
        self.machine.add_transitions = (trigger = 'wake_up', source = 'ligar', dest = 'crise_existencial')

        #A crise existencial do robo passou, agora ele vai procurar pela manteiga
        self.machine.add_transitions = (trigger = 'where_butter', source = '*', dest = 'procurar_manteiga')

        #Sabendo a localização da manteiga, o robo vai ate ela
        self.machine.add_transitions = (trigger = 'seeking_butter', source = '*', dest = 'buscar_manteiga')

        #Apos chegar até o destino o robo vai passar a manteiga
        self.machine.add_transitions = (trigger = 'buterry', source = 'buscar_manteiga', dest = 'passar_manteiga')

        #Após cumprir seu objetivo, o robo voltará a dormir
        self.machine.add_transitions = (trigger = 'sleep', source = 'passar_manteiga', dest = 'desligar')

    #Subscriber da visao
    def visionCallback(self, msg):
        self.x_centro = msg.x_centro
        self.y_centro = msg.y_centro
        self.roi_altura = msg.roi_altura
        self.roi_largura = msg.roi_largura
        self.manteiga_encontrada = msg.manteiga_encontrada

    #Publisher do movimento
    def publishToMov(self):
        msg_mov = Behav_mov()
        msg_mov.move = self.movimento
        self.pubMov.publish(msg_mov)

    #Publisher da Visão
    def publishToVis(self):
        print(self.rede_neural_ligada)
        msg_vis = Behav_vis()
        msg_vis.rede_neural_ligada = self.rede_neural_ligada
        self.pubVis.publish(msg_vis)

    #MÉTODO PARA PRINTAR AS VARIAVEIS
    def toString(self):
        print('Posição da manteiga: (' + str(self.x_centro) + ',' + str(self.y_centro) + ')')
        print('Largura da manteiga:' + str(self.roi_largura))
        print('Altura da manteiga:' + str(self.roi_altura))
        print('Manteiga encontrada:' + str(self.manteiga_encontrada))
        print('Rede neural ligada:' + str(self.rede_neural_ligada))
        print('Movimento que esta sendo executado:' + str(self.movimento))

    #MÉTODOS REFERENTES AO MOVIMENTO
    def move_forward(self);
        #Método responsável pelo robo se mover para frente
        self.movimento = 'move_forward'
        print('Robo esta se movimentando para frente\n')

    def walk_back(self):
        #Método responsável pelo robo se mover para tras
        self.movimento = 'walk_back'
        print('Robo esta se movimentando para tras\n')

    def rotate_time(self):
        #Método responsavel pelo robo girar no sentido horario
        self.movimento = 'rotate_clockwise'
        print('Robo está girando no sentido horario\n')

    def rotate_counterclockwise(self):
        #Método responsável pelo robo girar no sentido antihorario
        self.movimento = 'rotate_counterclockwise'
        print('Robo está girando no sentido antihorario\n')

    def butter(self):
        #Método responsável pelo robo passar a manteiga
        self.movimento = 'move_butter'
        print('Robo esta passando a manteiga\n')

    #MÉTODOS REFERENTES A VISÃO
    def connect_neural_network(self):
        #Método responsável por conectar a rede neural
        self.rede_neural_ligada = True
        print('Ligando a rede neural\n')

    def turn_off_neural_network(self):
        #Método responsável para desligar a rede neural
        self.rede_neural_ligada = False
        print('Desligando a rede neural\n')

    def alignment(self):
        if(self.x_centro > 0):
            print('Manteiga esta para a direita\n')
            return 'direita'

        elif(self.x_centro < 0):
            print('Manteiga esta para a esquerda\n')
            return 'esquerda'

        else:
            print('Manteiga esta no centro\n')
            return 'centro'

    def close_enough(self):
        if(self.roi_largura > 5):
            print('A manteiga esta proxima o suficiente\n')
            return True
        
        else:
            print('A manteiga não esta próxima o suficiente\n')
            return False

    def checkEssentialParam(self):
        if(self.manteiga_encontrada == False):
            if(self.states = 'live' or self.states = 'crise_existencial'):
                pass
            else:
                self.where_butter()

        elif(self.alignment != 'centro' or self.close_enough == False):
            self.seeking_butter()
            
        else:
            pass
    
def brain():
    robot = Robot('passador de manteiga')
    while not rospy.is_shutdown():
        robot.checkEssentialParam()
        robot.publishToMov()
        robot.publishToVis()
        robot.toString()

        if(robot.states == 'ligar'):
            os.system('clear')
            print('---------ESTADO ATUAL:' + robot.states + '-------\n\n')
            print('Inicializando o Behaviour')
            robot.connect_neural_network()
            time.sleep(3)
            robot.wake_up()

        elif(robot.states == 'crise_existencial'):
            os.system('clear')
            print('---------ESTADO ATUAL:' + robot.states + '-------\n\n')
            print('OH nao, estou tendo uma crise existencial!!!\n')
            robot.where_butter()

        elif(robot.states == 'procurar_manteiga'):
            os.system('clear')
            print('---------ESTADO ATUAL:' + robot.states + '-------\n\n')
            print('Procurando pela manteiga')
            robot.rotate_time()
            if(robot.manteiga_encontrada):
                robot.seeking_butter()

        elif(robot.states == 'buscar_manteiga'):
            os.system('clear')
            print('---------ESTADO ATUAL:' + robot.states + '-------\n\n')
            alignment = robot.alignment()

            if(alignment == 'direita'):
                robot.rotate_time()

            elif(alignment == 'esquerda'):
                robot.rotate_counterclockwise()

            else:
                if(robot.close_enough()):
                    robot.buterry()
                else:
                    robot.move_forward()

        elif(robot.states == 'passar_manteiga'):
            os.system('clear')
            print('---------ESTADO ATUAL:' + robot.states + '-------\n\n')
            robot.butter()
            robot.turn_off_neural_network()
            robot.sleep()

        elif(robot.states == 'desligar'):
            os.system('clear')
            print('---------ESTADO ATUAL:' + robot.states + '-------\n\n')
            print('Objetivo concluido\n')
            print('A mimir\n')
            time.sleep(3)
            break

        else:
            break

def main():
    rospy.init_node('state_node', anonymous = True)
    brain()
    rospy.spin()

main()