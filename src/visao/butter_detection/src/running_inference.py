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


def rodando_rede(net, output_layers, frame):
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
            color = (255, 0, 0)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.rectangle(frame, (x, y), (x + w, y + 15), color, -1)
            x_centro, y_centro, roi_largura, roi_altura = int(x + w/2), int(y + h/2), w, h
            cv2.putText(frame, label + " " + str(round(confidence, 2)), (x, y + 15), cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255), 1)
    
    return frame, manteiga_encontrada, x_centro, y_centro, roi_largura, roi_altura