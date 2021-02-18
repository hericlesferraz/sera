#include "simple_moves.h"

robotControl::robotControl()
{
    ros::Subscriber getName = nh.subscribe("model_name", 100, &robotControl::getNameCallback, this);
    while(robotName == " "){
        ros::spinOnce();
    }
    getName.shutdown();

    getFloat.request.ask = false;

    commandAssociation.insert(std::pair<std::string,int>("move_forward",1));
    commandAssociation.insert(std::pair<std::string,int>("walk_back",2));
    commandAssociation.insert(std::pair<std::string,int>("rotate_clockwise",3));
    commandAssociation.insert(std::pair<std::string,int>("rotate_counterclockwise",4));

    behav2Mov = nh.subscribe("behaviour_movimento", 100, &robotControl::behav2MovCallback, this);
}

void robotControl::getNameCallback(const std_msgs::String::ConstPtr &model)
{
    robotName = model->data.c_str();
    return;
}

void robotControl::behav2MovCallback(const std_msgs::String::ConstPtr &req)
{
    switch(commandAssociation[req->data]){
        case 1:
            moveWheels(req->data);
            break;
        case 2:
            moveWheels(req->data);
            break;
        case 3:
            moveWheels(req->data);
            break;
        case 4:
            moveWheels(req->data);
            break;
        default:
            break;
    }
}

bool robotControl::sendPosition(std::string motor, float requisition)
{
    sendRequisitionFloat.request.value = requisition;
    positionClient = nh.serviceClient<robot_moves::set_float>(robotName+"/"+motor+"/set_position");

    return positionClient.call(sendRequisitionFloat);
}

int main(int argc, char **argv)
{
    ros::init(argc, argv, "movementSimple_moves");
    robotControl controller();

    ros::spin();

    return 0;
}