#!/usr/bin/env python3


import rospy
import os

from transitions import Machine
import time
import csv

from state_machine.msg import Behav_mov
from state_machine.msg import Behav_vis
from butter_detection.msg import visparabeh

class Robot(object):

    states = ['ligar', 'crise_existencial', 'procurar_por_manteiga', 'buscar_manteiga', 'passar_manteiga', 'desligar']

    def __init__(self, name):

        # Define o nome do seu robô que passa manteiga!
        self.name = name

        #Define um Subscriber (ROS)
        self.subVis = rospy.Subscriber('visao_behaviour', visparabeh, self.visionCallback)

        #Define um Publisher (ROS)
        self.pubMov = rospy.Publisher('behaviour_movimento', Behav_mov, queue_size=100)
        self.pubVis = rospy.Publisher('behaviour_visao', Behav_vis, queue_size=100)

        #Define vairáveis que serão utilizadas
        self.x_centro = 0
        self.y_centro = 0
        self.roi_largura = 0
        self.roi_altura = 0
        self.manteiga_encontrada = False
        self.rede_neural_ligada = False 
        self.movimento = 'init_position'

        

        # Iniciliza a maquina de estados
        self.machine = Machine(model=self, states=Robot.states, initial='ligar')

        # Toda manha ao acordar nosso robô irá ter uma crise existencial
        self.machine.add_transition(trigger='wake_up', source='ligar', dest='crise_existencial')

        # Após finalizar a crise existencial, ele deve procurar pela manteiga
        self.machine.add_transition(trigger='where_butter', source='*', dest='procurar_por_manteiga')

        # Após saber a localização da manteiga, ele deve chegar até a manteiga
        self.machine.add_transition(trigger='seeking_the_butter', source='*', dest='buscar_manteiga')

        # Agora que o robô já está na manteiga, vamos pega-la
        self.machine.add_transition(trigger='buterry', source='buscar_manteiga', dest='passar_manteiga')
        
        #Agora que o robô concluiu seu objetivo, vamos desliga-lo
        self.machine.add_transition(trigger='sleep', source='passar_manteiga', dest='desligar')

    #*MÉTODO QUE EXIBE NO TERMINAL TODAS OS PARÂMETROS
    def toString(self):
        print('Posicão da Manteiga: (' + str(self.x_centro) + ',' + str(self.y_centro) + ')')
        print('Largura da Manteiga: ' + str(self.roi_largura))
        print('Altura da Manteiga: ' + str(self.roi_altura))
        print('Manteiga encontrada: ' + str(self.manteiga_encontrada))
        print('Rede Neural Liga: ' + str(self.rede_neural_ligada))
        print('Movimento sendo executado: ' + str(self.movimento))

    #*SUBSCRIBER DA VISÃO
    def visionCallback(self, msg):
        self.x_centro = msg.x_centro
        self.y_centro = msg.y_centro
        self.roi_largura = msg.roi_largura
        self.roi_altura = msg.roi_altura
        self.manteiga_encontrada = msg.manteiga_encontrada
    
    #*PUBLISHER PARA O MOVIMENTO
    def publishToMov(self):
        msg_mov = Behav_mov()
        msg_mov.move = self.movimento
        self.pubMov.publish(msg_mov)

    #*PUBLISHER PARA A VISÃO
    def publishToVis(self):
        print(self.rede_neural_ligada)
        msg_vis = Behav_vis()
        msg_vis.rede_neural_ligada = self.rede_neural_ligada
        self.pubVis.publish(msg_vis)

    #*MÉTODOS MOVIMENTO 
    def move_forward(self):
        #*Movimento para o robô se deslocar para frente
        self.movimento = 'move_forward'
        print('Robô se movimento para frente\n')

    def walk_back(self):
        #*Movimento para o robô se deslocar para trás
        self.movimento = 'walk_back'
        print('Robô se movimentando para trás\n')

    def rotate_time(self):
        #*Movimento para o robô rotacionar em sentido horário
        self.movimento = 'rotate_clockwise'
        print('Robô rotacionando no sentido horário\n')

    def rotate_counterclockwise(self):
        #*Movimento para o robô rotacionar em sentido anti-horário
        self.movimento = 'rotate_counterclockwise'
        print('Robô rotacionando no sentido anti-horário\n')
    
    def butter(self):
        #*Movimento para o robô "passar manteiga"
        self.movimento = 'move_butter'
        print('Robô passando manteiga\n')

    #*MÉTODOS - VISÃO
    def connect_neural_network(self):
        #*Ligar a rede neural
        self.rede_neural_ligada = True
        print('Ligando rede neural\n')

    def turn_off_neural_network(self):
        #*Desligar a rede neural
        self.rede_neural_ligada = False
        print('Desligando rede neural\n')

    def alignment(self):
        #*Confere o alinhamento da manteiga em ralação ao centro da robô
        if(self.x_centro > 258):
            print('Alinhamento da manteiga para direita\n')
            return 'direita'
        elif(self.x_centro < 158):
            print('Alinhamento da manteiga para esquerda\n')
            return 'esquerda'
        else:
            print('Alinhamento da manteiga centralizado\n')
            return 'centro'
    
    def close_enough(self):
        #*Confere se a manteiga está perto o suficiente
        if(self.roi_largura > 250):
            print('Manteiga perto o suficiente\n')
            return True
        else:
            print('Manteiga não está perto o suficiente\n')
            return False

    def checkEssentialParam(self):
        if(self.manteiga_encontrada == False):
            if(self.state == 'ligar' or self.state == 'crise_existencial'):
                pass
            else:
                self.where_butter()
        elif(self.alignment() != 'centro' or self.close_enough() == False):
            self.seeking_the_butter()
        else:
            pass

#*MÉTODO QUE EXECUTA TODA A LÓGICA DO BEHAVIOUR
def brain():
    robot = Robot('passador de manteiga')
    while not rospy.is_shutdown():
        time.sleep(1)
        robot.checkEssentialParam() #Conferindo se os parâmetros essenciais estão corretos
        robot.publishToMov() #Publicando variáveis para o movimento
        robot.publishToVis() #Publicando variáveis para a visão
        robot.toString() #Exibindo no terminal as variáveis
        if(robot.state == 'ligar'):
            os.system('clear') #Limpando o terminal
            print('------ESTADO ATUAL:' + robot.state + '------\n\n')
            print('Iniciando behaviour...\n')
            robot.connect_neural_network() #Chamando método que liga a rede neural
            time.sleep(3)
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
            robot.sleep()

        elif(robot.state == 'desligar'):
            os.system('clear') #Limpando o terminal
            print('------ESTADO ATUAL:' + robot.state + '------\n\n')
            print('Objetivo concluído!')
            time.sleep(3)
            break

        else:
            break

def main():
    rospy.init_node('state_node', anonymous=True)
    brain()
    rospy.spin()
    
main()