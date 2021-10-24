import os
import cv2
import random
import time
import numpy as np

def get_cnn_files():
    detection_folder = os.path.join(os.path.expanduser('~'), "Youtube/sera/src/visao/butter_detection")
    weights_folder = os.path.join(detection_folder, "weights")

    config_file = os.path.join(weights_folder, "yolov4-tiny-obj.cfg")
    weights_file = os.path.join(weights_folder, "yolov4-tiny-obj_best.weights")

    return read_cnn_architecture(config_file, weights_file)

def read_cnn_architecture(config_file, weights_file):
    net = cv2.dnn.readNet(config_file, weights_file, "darknet")

    return net

def set_model_input(net):
    model = cv2.dnn_DetectionModel(net)
    model.setInputParams(size = (416, 416), scale = 1/255, swapRB = True)

    return model

def detect_model(model, current_frame):
    if random.randint(1, 3) == 2:
        start_time = time.time()
        classes, scores, boxes = model.detect(current_frame, 0.6, 0.4)
        finish_time = time.time()

        fps = 1 / (finish_time - start_time)
        print("FPS: ", fps)

        if isinstance(classes, np.ndarray):
            manteiga_encontrada = True
        elif isinstance(classes, tuple):
            manteiga_encontrada = False

        return classes, scores, boxes, int(fps), manteiga_encontrada

def draw_results(frame, classes, scores, boxes):
    for i in range(len(boxes)):
        [x_top, y_top, roi_width, roi_height] = boxes[i]
        p1 = (x_top, y_top)
        p2 = (x_top + roi_width, y_top + roi_height)
        p3 = (x_top, y_top - 5)

        cv2.rectangle(frame, p1, p2, color = (255, 0, 0), thickness = 2)

        confidence = str(round(float(scores[i][0]), 2))
        if classes[i][0] == 0:
            label = "Butter"

        cv2.putText(frame, label + " " + confidence, p3, cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), thickness = 1)

        