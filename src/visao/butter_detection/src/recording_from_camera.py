#!/usr/bin/python3
import rospy
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
import cv2

class Listener():
    
    def __init__(self):
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.writer = cv2.VideoWriter('video.avi', fourcc, 30.0, (416, 416))

        rospy.init_node("videoRecorder", anonymous = True)
        rospy.Subscriber("/ButterRobotLargeBaseUrdf_13461_victor_Nitro_AN515_51/cam_Link/image",
                         Image, self.callback_method)
        rospy.spin()

    def callback_method(self, msg):
        bridge = CvBridge()
        self.frame = bridge.imgmsg_to_cv2(msg, desired_encoding = 'bgr8')

        cv2.imshow("Camera", self.frame)
        self.writer.write(self.frame)

        if cv2.waitKey(1) == ord('q'):
            self.finish_video()

    def finish_video(self):
        self.writer.release()
        cv2.destroyAllWindows()
        rospy.signal_shutdown("ROS finished")


if __name__ == '__main__':
    Listener()