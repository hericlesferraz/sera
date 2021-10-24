import os
import cv2

os.chdir("../dataset/video")
cap = cv2.VideoCapture("video.avi")

current_frame = 0
while(True):
    ret, frame = cap.read()

    name = '../frames/manteiga_' + str(current_frame) + '.jpg'

    if current_frame % 20 == 0:
        print("Creating " + name)
        cv2.imwrite(name, frame)

    current_frame += 1

cap.release()
cv2.destroyAllWindows()