#include "simple_moves.h"

robotControl::robotControl()
{
    ros::Subscriber getName = nh.subscribe("model_name", 100, &robotControl::getNameCallback, this);
    while(robotName == " "){
        ros::spinOnce();
    }
    getName.shutdown();

    sendRequisitionFloat.request.value = 10;
    for(int i = 0; i < 11; i++){
        velocityClient = nh.serviceClient<robot_moves::set_float>(robotName+"/"+motorNames[i]+"/set_velocity");
        velocityClient.call(sendRequisitionFloat);
    }

    getFloat.request.ask = true;

    behav2Mov = nh.subscribe("behaviour_movimento", 10, &robotControl::behav2MovCallback, this);
}

void robotControl::getNameCallback(const std_msgs::String::ConstPtr &model)
{
    robotName = model->data.c_str();
    return;
}

void robotControl::behav2MovCallback(const robot_moves::Behav_mov::ConstPtr &message)
{
    execMove(message->move);
    return;
}

bool robotControl::sendPosition(std::string motor, float requisition)
{
    sendRequisitionFloat.request.value = requisition;

    positionClient = nh.serviceClient<robot_moves::set_float>(robotName+"/"+motor+"/set_position");
    
    return positionClient.call(sendRequisitionFloat);
}

bool robotControl::moveWheels(std::string wheel, bool request, std::string movement)
{
    if(movement == "move_forward" || movement == "walk_back")
    {
        add = translateAdd;
    }else 
        add = rotationAdd;

    gpositionClient = nh.serviceClient<robot_moves::get_float>("/"+robotName+"/"+wheel+"/get_target_position");
    gpositionClient.call(getFloat);

    getFloat.response.value += (request) ? add : -add;
    
    return sendPosition(wheel , getFloat.response.value);
} 

int main(int argc, char **argv)
{
    ros::init(argc, argv, "movementSimple_moves");

    robotControl *controller = new robotControl();

    //controller->testMode();

    ros::spin();

    return 0;
}