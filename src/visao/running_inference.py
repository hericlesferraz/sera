import os
import cv2

# Lendo a rede neural com o OpenCV
os.chdir("Melhor CNN")
net = cv2.dnn.readNet("yolov4-tiny-obj.cfg", "yolov4-tiny-obj_best.weights", "darknet")
outNames = net.getUnconnectedOutLayersNames()
os.chdir("..")

# Criando um blob a partir de um frame
image = cv2.imread("teste.jpg")
print(image.shape)
blob = cv2.dnn.blobFromImage(image, size = (416, 416))
print(blob.shape)

# Rodando o modelo
net.setInput(blob, scalefactor = 1/255.0)
outs = net.forward(outNames)
print(outs)
print(outs.shape)
boxes = []
confidences = []
classIDs = []


# Entendendo o resultado
for output in outs:
    # loop over each of the detections
    for detection in output:
        # extract the class ID and confidence (i.e., probability)
        # of the current object detection
        scores = detection[5:]
        classID = np.argmax(scores)
        confidence = scores[classID]
        # filter out weak predictions by ensuring the detected
        # probability is greater than the minimum probability
        if confidence > args["confidence"]:
            # scale the bounding box coordinates back relative to
            # the size of the image, keeping in mind that YOLO
            # actually returns the center (x, y)-coordinates of
            # the bounding box followed by the boxes' width and
            # height
            box = detection[0:4] * np.array([W, H, W, H])
            (centerX, centerY, width, height) = box.astype("int")
            # use the center (x, y)-coordinates to derive the top
            # and and left corner of the bounding box
            x = int(centerX - (width / 2))
            y = int(centerY - (height / 2))
            # update our list of bounding box coordinates,
            # confidences, and class IDs
            boxes.append([x, y, int(width), int(height)])
            confidences.append(float(confidence))
            classIDs.append(classID)