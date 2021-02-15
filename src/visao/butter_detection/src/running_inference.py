#!/usr/bin/python3
import os
import cv2
import numpy as np

# Lendo a rede neural com o OpenCV
def ler_rede():
    os.chdir(os.path.join(os.path.expanduser("~"), "sera/src/visao/butter_detection/src"))
    net = cv2.dnn.readNet("yolov4-tiny-obj.cfg", "yolov4-tiny-obj_first_best.weights", "darknet")
    outNames = net.getUnconnectedOutLayersNames()
    os.chdir("..")

    return net, outNames

# Criando um blob a partir de um frame
def fazendo_blob_e_configurando_input(net, image):
    blob = cv2.dnn.blobFromImage(image, size = (416, 416))

    net.setInput(blob, scalefactor = 1/255.0)
    return net


def rodando_rede(net, output_layers):
    (manteiga_encontrada, x_centro, y_centro, roi_largura, roi_altura) = (False, -1, -1, -1, -1) 
    width, height = 416, 416
    classes = ["butter"]
    outs = net.forward(output_layers)
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.2:
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.4, 0.3)
    for i in range(len(boxes)):
        if i in indexes:
            manteiga_encontrada = True
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            confidence = confidences[i]
            #color = (255, 0, 0)
            #cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            #cv2.rectangle(frame, (x, y), (x + w, y + 15), color, -1)
            x_centro, y_centro, roi_largura, roi_altura = int(x + w/2), int(y + h/2), w, h
            #cv2.putText(frame, label + " " + str(round(confidence, 2)), (x, y + 15), cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255), 1)
    
    return manteiga_encontrada, x_centro, y_centro, roi_largura, roi_altura

def organizando_array(last_seven_manteiga_encontrada, manteiga_encontrada, last_seven_x_centro, x_centro, last_seven_y_centro, y_centro, last_seven_roi_largura, roi_largura, last_seven_roi_altura, roi_altura):
    last_att_manteiga_encontrada = np.full(7, False)
    last_att_x_centro = np.full(7, 0, dtype = np.int16)
    last_att_y_centro = np.full(7, 0, dtype = np.int16)
    last_att_roi_largura = np.full(7, 0, dtype = np.int16)
    last_att_roi_altura = np.full(7, 0, dtype = np.int16)
    
    last_att_manteiga_encontrada[:-1] = last_seven_manteiga_encontrada[1:].copy()
    last_att_manteiga_encontrada[-1] = manteiga_encontrada

    last_att_x_centro[:-1] = last_seven_x_centro[1:].copy()
    last_att_x_centro[-1] = x_centro
    print(last_seven_x_centro)
    print(x_centro)
    print(last_att_x_centro)

    last_att_y_centro[:-1] = last_seven_y_centro[1:].copy()
    last_att_y_centro[-1] = y_centro

    last_att_roi_largura[:-1] = last_seven_roi_largura[1:].copy()
    last_att_roi_largura[-1] = roi_largura

    last_att_roi_altura[:-1] = last_seven_roi_altura[1:].copy()
    last_att_roi_altura[-1] = roi_altura

    return last_att_manteiga_encontrada, last_att_x_centro, last_att_y_centro, last_att_roi_largura, last_att_roi_altura

def fazendo_media_e_desenhando_bb(frame, last_seven_manteiga_encontrada, last_seven_x_centro, last_seven_y_centro, last_seven_roi_largura, last_seven_roi_altura):
    # Se um dos sete valores para manteiga_encontrada for True
    if np.any(last_seven_manteiga_encontrada[:] == True) == True:
        #manteiga_encontrada = True

        selecao_x_centro = last_seven_x_centro.copy()
        selecao_x_centro = selecao_x_centro[selecao_x_centro >= 0]
        selecao_y_centro = last_seven_y_centro.copy()
        selecao_y_centro = selecao_y_centro[selecao_y_centro >= 0]
        selecao_roi_largura = last_seven_roi_largura.copy()
        selecao_roi_largura = selecao_roi_largura[selecao_roi_largura >= 0]
        selecao_roi_altura = last_seven_roi_altura.copy()
        selecao_roi_altura = selecao_roi_altura[selecao_roi_altura >= 0]

        x_centro = int(np.mean(selecao_x_centro))
        y_centro = int(np.mean(selecao_y_centro))
        roi_largura = int(np.mean(selecao_roi_largura))
        roi_altura = int(np.mean(selecao_roi_altura))

        color = (255, 0, 0)
        w = roi_largura
        h = roi_altura
        x = int(x_centro - w/2)
        y = int(y_centro - h/2)

        #print(last_seven_x_centro, last_seven_y_centro)
        #print(x, y, w, h)
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        cv2.rectangle(frame, (x, y), (x + w, y + 15), color, -1)
    
        return frame, last_seven_manteiga_encontrada, last_seven_x_centro, x_centro, last_seven_y_centro, y_centro, last_seven_roi_largura, roi_largura, last_seven_roi_altura, roi_altura

    return frame, last_seven_manteiga_encontrada, last_seven_x_centro, -1, last_seven_y_centro, -1, last_seven_roi_largura, -1, last_seven_roi_altura, -1