#!/usr/bin/python3
# coding=utf-8
import running_inference as ri

import cv2
from cv_bridge import CvBridge

import rospy
from sensor_msgs.msg import Image as ROS_Image
from butter_detection.msg import visparabeh
from std_msgs.msg import String
from butter_detection.srv import set_int

class Node():

    def __init__(self):
        rospy.init_node("visao", anonymous = True)
        self.net = ri.get_cnn_files()
        self.model = ri.set_model_input(self.net)
        
        self.classes = [[]]
        self.scores = [[]]
        self.boxes = []
        self.butter_found = False
        self.x_top, self.y_top, self.roi_width, self.roi_height = -1, -1, -1, -1

        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

        self.topic_substring = rospy.wait_for_message("/model_name", String)
        self.topic_substring = self.topic_substring.data
        
        self.enable_camera_service()
        self.enable_success = self.enable_success.success
        if self.enable_success == True:
            self.image_topic = "/" + self.topic_substring + "/cam_Link/image"
            rospy.Subscriber(self.image_topic, ROS_Image, self.convert_ROS_Image_to_cv2)
            self.publisher = rospy.Publisher("visao_behaviour", visparabeh, queue_size = 100)
            rospy.spin()

    def enable_camera_service(self):
        self.enable_service = "/" + self.topic_substring + "/cam_Link/enable"
        rospy.wait_for_service(self.enable_service)

        try:
            self.enable_camera_client = rospy.ServiceProxy(self.enable_service, set_int)
            self.enable_success = self.enable_camera_client(1)
            
        except Exception:
            print("Service call failed.")

    def convert_ROS_Image_to_cv2(self, image):
        self.opencv_bridge = CvBridge()

        try:
            self.current_frame = self.opencv_bridge.imgmsg_to_cv2(image, desired_encoding = "bgr8")

        except Exception as e:
            print(e)

        self.send_current_frame_to_inference()

    def send_current_frame_to_inference(self):
        try:
            self.classes, self.scores, self.boxes, self.fps, self.butter_found = ri.detect_model(self.model,
                                                                                                 self.current_frame)
        except Exception:
            pass
        
        self.show_result_frame()
        self.publish_results()

    def show_result_frame(self):
        
        ri.draw_results(self.current_frame, self.classes, self.scores, self.boxes)

        cv2.imshow("Current Frame", self.current_frame)
        cv2.waitKey(1)

    def publish_results(self):
        self.vision_msg = visparabeh()

        self.vision_msg.manteiga_encontrada = self.butter_found

        if self.butter_found == True:
            for i in range(len(self.boxes)):
                [self.x_top, self.y_top, self.roi_width, self.roi_height] = self.boxes[i]

        elif self.butter_found == False:
            self.x_top, self.y_top, self.roi_width, self.roi_height = -1, -1, -1, -1

        self.x_center = int(self.x_top + (self.roi_width/2))
        self.y_center = int(self.y_top + (self.roi_height/2))

        self.vision_msg.x_centro = self.x_center
        self.vision_msg.y_centro = self.y_center
        self.vision_msg.roi_largura = self.roi_width
        self.vision_msg.roi_altura = self.roi_height

        self.publisher.publish(self.vision_msg)


no_visao = Node()