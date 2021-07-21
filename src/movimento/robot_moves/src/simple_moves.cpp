#include "simple_moves.h"

robotControl::robotControl()
{
    ros::Subscriber getName = nh.subscribe("model_name", 100, &robotControl::getNameCallback, this);
    while(robotName == " "){
        ros::spinOnce();
    }
    getName.shutdown();

    sendRequisitionFloat.request.value = 2;
    for(int i = 0; i < 11; i++){
        velocityClient = nh.serviceClient<robot_moves::set_float>(robotName+"/"+motorNames[i]+"/set_velocity");
        velocityClient.call(sendRequisitionFloat);
    }

    getFloat.request.ask = true;
}

void robotControl::getNameCallback(const std_msgs::String::ConstPtr &model)
{
    robotName = model->data.c_str();
    return;
}

bool robotControl::sendPosition(std::string motor, float requisition)
{
    sendRequisitionFloat.request.value = requisition;

    positionClient = nh.serviceClient<robot_moves::set_float>(robotName+"/"+motor+"/set_position");
    
    return positionClient.call(sendRequisitionFloat);
}

bool robotControl::moveWheels(std::string wheel, bool request){

    gpositionClient = nh.serviceClient<robot_moves::get_float>("/"+robotName+"/"+wheel+"/get_target_position");
    gpositionClient.call(getFloat);

    getFloat.response.value += (request) ? 3.14/4 : -3.14/4;
    
    return sendPosition(wheel , getFloat.response.value);
} 

int main(int argc, char **argv)
{
    ros::init(argc, argv, "movementSimple_moves");

    robotControl *controller = new robotControl();

    for(int i = 0; i < 100; i++)
    {
        controller->moveWheels("wheel_left_front",1);
        controller->moveWheels("wheel_left_back",1);

        controller->moveWheels("wheel_right_front",1);
        controller->moveWheels("wheel_right_back",1);
    }

    ros::spin();

    return 0;
}