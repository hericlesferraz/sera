#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import sys
import time
import rospy

from butter_detection.msg import visparabeh
from pygame.locals import *

pygame.init()

class Ballsim(object):
    def __init__(self):
        self.found = True
        self.imageWidth = 160
        self.imageHeight = 160

        self.FPS = 30
        self.fpsClock=pygame.time.Clock()

        ##Tamanho do display
        self.size = (640, 480)

        ##Cria o display
        self.DISPLAYSURF=pygame.display.set_mode(self.size)

        ##Título do display
        pygame.display.set_caption('Behaviour_test')

        ##Carregando a imagem do fundo
        self.background = pygame.image.load('background.jpg')

        ##Carrega a imagem que vai mexer
        self.coord = pygame.image.load('bola2.png')

        ##quando direction=None a imagem ficará parada
        self.direction=None

        ''' coord_x e coord_y são as coordenadas iniciais da imagem que iremos movimentar, onde 
            (0,0) é o canto superior esquerdo e os eixos crescem para a direita e para baixo'''
        self.coord_x = 0
        self.coord_y = 0

        #Subscrevendo o tópico da Visão
        self.pub = rospy.Publisher('visao_behaviour', visparabeh, queue_size=100)

        self.execute()

    def execute(self):
        while True:
            ##'Desenha' o display
            self.DISPLAYSURF.blit(self.background,(0,0))
            self.DISPLAYSURF.blit(self.coord,(self.coord_x,self.coord_y))

            ''' event é uma propriedade da biblioteca;
                ".get" pega um evento da fila, todo evento é um objeto 
                que possui o atributo type.
                keydown e keyup são os eventos quando as teclas estão 
                sendo pressionadas e quando são soltas.'''
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    self.direction = event.key
                        
                if event.type == pygame.KEYUP:
                    if (event.key == self.direction):
                        self.direction = None
            
            ##atualiza as coordenadas
            self.coord_x, self.coord_y = self.move()

            #Atualiza o found
            if(self.coord_x < -self.imageWidth or self.coord_y < -self.imageHeight or self.coord_x > self.size[0] or self.coord_y > self.size[1]):
                self.found = False
            else:
                self.found = True

            pygame.display.update()
            self.fpsClock.tick(self.FPS)
            self.publish()

    def move(self):
        ''' pygame tem as constantes padrões pras teclas;
            essas que eu usei são correspondentes as setinhas do teclado '''
        if self.direction:
            if self.direction == pygame.K_UP:
                self.coord_y -= 20
                
            elif self.direction == pygame.K_DOWN:
                self.coord_y += 20
                
            if self.direction == pygame.K_LEFT:
                self.coord_x -= 20
                
            elif self.direction == pygame.K_RIGHT:
                self.coord_x += 20
                
        return self.coord_x, self.coord_y
    
    def publish(self):
        msg = visparabeh()
        msg.roi_altura = self.imageHeight
        msg.roi_largura = self.imageWidth
        msg.x_centro = self.coord_x + int((self.imageWidth)/2)
        msg.y_centro = self.coord_y + int((self.imageHeight)/2)
        msg.manteiga_encontrada = self.found

        self.pub.publish(msg)

if __name__ == '__main__':
    rospy.init_node('Ballsim', anonymous=True)

    ballsim = Ballsim()

    rospy.spin()
