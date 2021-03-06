#!/usr/bin/python3
from butter_detection.msg import visparabeh
from state_machine.msg import Behav_vis
import os
import subprocess
import rospy
from sensor_msgs.msg import Image as TipoMensagemImagem
from cv_bridge import CvBridge
import cv2
import numpy as np
import running_inference as ri
import time
import numpy

def listening_to_behaviour(msg):
    global rede_neural_ligada
    rede_neural_ligada = msg.rede_neural_ligada

# Subscrevendo no tópico da câmera
def listener():
    primeira_iteracao = True

    global last_seven_manteiga_encontrada
    global last_seven_x_centro
    global last_seven_y_centro
    global last_seven_roi_largura
    global last_seven_roi_altura
    global label
    global confidence

    last_seven_manteiga_encontrada = np.full(7, False)
    last_seven_x_centro = np.full(7, 0, dtype = np.int16)
    last_seven_y_centro = np.full(7, 0, dtype = np.int16)
    last_seven_roi_largura = np.full(7, 0, dtype = np.int16)
    last_seven_roi_altura = np.full(7, 0, dtype = np.int16)
    label = "butter"
    confidence = 0.0

    rospy.Subscriber(topicos[index_topico_camera], TipoMensagemImagem, callback, callback_args=(primeira_iteracao, last_seven_manteiga_encontrada, last_seven_x_centro, last_seven_y_centro, last_seven_roi_largura, last_seven_roi_altura, label, confidence))
    rospy.spin()

# Função de callback
def callback(data, tuple):
    primeira_iteracao, last_seven_manteiga_encontrada, last_seven_x_centro, last_seven_y_centro, last_seven_roi_largura, last_seven_roi_altura, label, confidence = tuple[:]
    starting_time = time.time()
    bridge = CvBridge()
    cv_image = bridge.imgmsg_to_cv2(data, desired_encoding='bgr8')
    rede_configurada = ri.fazendo_blob_e_configurando_input(rede, cv_image)

    manteiga_encontrada, x_centro, y_centro, roi_largura, roi_altura, label, confidence = ri.rodando_rede(rede_configurada, camadas, label, confidence)

    last_seven_manteiga_encontrada, last_seven_x_centro, last_seven_y_centro, last_seven_roi_largura, last_seven_roi_altura = ri.organizando_array(last_seven_manteiga_encontrada, manteiga_encontrada, last_seven_x_centro, x_centro, last_seven_y_centro, y_centro, last_seven_roi_largura, roi_largura, last_seven_roi_altura, roi_altura)
    frame, last_seven_manteiga_encontrada, manteiga_na_bounding_box, last_seven_x_centro, x_centro, last_seven_y_centro, y_centro, last_seven_roi_largura, roi_largura, last_seven_roi_altura, roi_altura = ri.fazendo_media_e_desenhando_bb(cv_image, last_seven_manteiga_encontrada, last_seven_x_centro, last_seven_y_centro, last_seven_roi_largura, last_seven_roi_altura, label, confidence)

    print(last_seven_manteiga_encontrada)
    print(last_seven_x_centro)

    cv2.imshow("Camera", frame)
    send_message(manteiga_na_bounding_box, x_centro, y_centro, roi_largura, roi_altura)
    print('''Manteiga = {}\nx_centro = {}\ny_centro = {}\nroi_largura = {}\nroi_altura = {}\n'''.format(manteiga_encontrada, x_centro, y_centro, roi_largura, roi_altura))
    elapsed_time = time.time() - starting_time
    print("FPS = {}\n".format(1/elapsed_time))

    global rede_neural_ligada
    if rede_neural_ligada == False:
        rospy.signal_shutdown("A Rede Neural foi desligada pelo Behaviour!")

    cv2.waitKey(1)

def send_message(manteiga_na_bounding_box, x_centro, y_centro, roi_largura, roi_altura):
    message_publisher = rospy.Publisher('visao_behaviour', visparabeh, queue_size = 100)

    message = visparabeh()
    message.manteiga_encontrada = manteiga_na_bounding_box
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

rospy.init_node('recebeImagemWebots', anonymous = True)
global rede_neural_ligada
rede_neural_ligada = False

while not rospy.is_shutdown():
    rede, camadas = ri.ler_rede()
    os.chdir(os.path.join(os.path.expanduser("~"), "darknet"))

    rospy.Subscriber("behaviour_visao", Behav_vis, listening_to_behaviour)

    if rede_neural_ligada == True:
        listener()
        rospy.spin()

    print("Rede Neural desligada!\n")
    rospy.init_node('recebeImagemWebots', anonymous = True)