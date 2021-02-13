#!/usr/bin/python3
from butter_detection.msg import visparabeh
import os
import subprocess
import rospy
from sensor_msgs.msg import Image as TipoMensagemImagem
from cv_bridge import CvBridge
import cv2
import numpy as np
import running_inference as ri
import time

# Subscrevendo no tópico da câmera
def listener():
    rospy.init_node('recebeImagemWebots', anonymous = True)
    rospy.Subscriber(topicos[index_topico_camera], TipoMensagemImagem, callback)  
    rospy.spin()

# Função de callback
def callback(data):
    starting_time = time.time()
    bridge = CvBridge()
    cv_image = bridge.imgmsg_to_cv2(data, desired_encoding='bgr8')
    rede_configurada = ri.fazendo_blob_e_configurando_input(rede, cv_image)
    frame, manteiga_encontrada, x_centro, y_centro, roi_largura, roi_altura = ri.rodando_rede(rede_configurada, camadas, cv_image)

    cv2.imshow("Camera", frame)
    send_message(manteiga_encontrada, x_centro, y_centro, roi_largura, roi_altura)
    print('''Manteiga = {}\nx_centro = {}\ny_centro = {}\nroi_largura = {}\nroi_altura = {}\n'''.format(manteiga_encontrada, x_centro, y_centro, roi_largura, roi_altura))
    elapsed_time = time.time() - starting_time
    print("FPS = {}\n".format(1/elapsed_time))
    cv2.waitKey(1)

def send_message(manteiga_encontrada, x_centro, y_centro, roi_largura, roi_altura):
    message_publisher = rospy.Publisher('visao_behaviour', visparabeh, queue_size = 100)

    message = visparabeh()
    message.manteiga_encontrada = manteiga_encontrada
    message.x_centro = x_centro
    message.y_centro = y_centro
    message.roi_largura = roi_largura
    message.roi_altura = roi_altura

    message_publisher.publish(message)


# Obtendo todos os serviços em funcionamento no momento
servicos = subprocess.check_output("rosservice list", shell = True)
servicos = servicos.decode('ascii')
servicos = servicos.split("\n")
print(servicos)
print()

# Obtendo o serviço da câmera e dando enable
ind = 0
index_servico_camera = 0
for servico in servicos:
    if "cam_Link/enable" in servico:
        index_servico_camera = ind
    ind += 1
print("Fornecendo True para o serviço camera/enable:")
print(servicos[index_servico_camera])
os.system('rosservice call {} "value: 1"'.format(servicos[index_servico_camera]))

# Obtendo todos os tópicos em funcionamento no momento
topicos = subprocess.check_output("rostopic list", shell = True)
topicos = topicos.decode('ascii')
topicos = topicos.split("\n")
print()
print(topicos)
print()

# Obtendo o tópico da câmera para se subscrever
ind = 0
index_topico_camera = 0
for topico in topicos:
    if "cam_Link/image" in topico:
        index_topico_camera = ind
    ind += 1
print("Subscrevendo no tópico da câmera:")
print(topicos[index_topico_camera])


if __name__ == '__main__':
    rede, camadas = ri.ler_rede()
    os.chdir(os.path.join(os.path.expanduser("~"), "darknet"))
    listener()