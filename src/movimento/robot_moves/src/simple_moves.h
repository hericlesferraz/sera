#ifndef SIMPLE_MOVES_H
#define SIMPLE_MOVES_H

#include "ros/ros.h"

#include "std_msgs/String.h"
#include "robot_moves/set_float.h"
#include "robot_moves/get_float.h"

class robotControl
{
    private:
    ros::NodeHandle nh;
    ros::ServiceClient gpositionClient, positionClient, velocityClient;

    robot_moves::set_float sendRequisitionFloat;
    robot_moves::get_float getFloat;

    std::string robotName = " ";
    std::string motorNames[11] = {"wheel_right_front","wheel_right_back","wheel_left_front","wheel_left_back","body","shoulder_right","elbow_right","hand_right","shoulder_left","elbow_left","hand_left"};

    public:
    //Construtor
    robotControl();
    
    //Funções apenas prototipadas no header
    void getNameCallback(const std_msgs::String::ConstPtr &model);
    bool sendPosition(std::string motor, float requisition);
    bool moveWheels(std::string wheel, bool request);
};

#endif