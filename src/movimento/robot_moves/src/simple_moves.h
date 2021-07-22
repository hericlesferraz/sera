#ifndef SIMPLE_MOVES_H
#define SIMPLE_MOVES_H

#include "ros/ros.h"

#include "std_msgs/String.h"
#include "robot_moves/set_float.h"
#include "robot_moves/get_float.h"

#include "robot_moves/Behav_mov.h"

#define translateAdd 3.141592*2;
#define rotationAdd 1.256/3;
class robotControl
{
    private:
    ros::NodeHandle nh;
    ros::ServiceClient gpositionClient, positionClient, velocityClient;
    ros::Subscriber behav2Mov;

    robot_moves::set_float sendRequisitionFloat;
    robot_moves::get_float getFloat;

    std::string robotName = " ";
    std::string motorNames[11] = {"wheel_right_front","wheel_right_back","wheel_left_front","wheel_left_back","body","shoulder_right","elbow_right","hand_right","shoulder_left","elbow_left","hand_left"};

    float add;

    public:
    //Construtor
    robotControl();
    
    //Funções apenas prototipadas no header
    void getNameCallback(const std_msgs::String::ConstPtr &model);
    void behav2MovCallback(const robot_moves::Behav_mov::ConstPtr &message);

    bool sendPosition(std::string motor, float requisition);
    bool moveWheels(std::string wheel, bool request, std::string movement);
    
    //Funções descritas no header, pois descrevem movimento
    void execMove(std::string moveToExecute)
    {
        if(moveToExecute == "move_forward")
        {
            moveWheels("wheel_left_front",  1, moveToExecute);
            moveWheels("wheel_left_back",  1, moveToExecute);

            moveWheels("wheel_right_front",  0, moveToExecute);
            moveWheels("wheel_right_back",  0, moveToExecute);                
        }
        else if(moveToExecute == "walk_back")
        {
            moveWheels("wheel_left_front",  0, moveToExecute);
            moveWheels("wheel_left_back",  0, moveToExecute);

            moveWheels("wheel_right_front",  1, moveToExecute);
            moveWheels("wheel_right_back",  1, moveToExecute);                
        }
        else if(moveToExecute == "rotate_clockwise")
        {
            moveWheels("wheel_left_front",  1, moveToExecute);
            moveWheels("wheel_left_back",  1, moveToExecute);

            moveWheels("wheel_right_front",  1, moveToExecute);
            moveWheels("wheel_right_back",  1, moveToExecute);                
        }
        else if(moveToExecute == "rotate_counterclockwise")
        {
            moveWheels("wheel_left_front",  0, moveToExecute);
            moveWheels("wheel_left_back",  0, moveToExecute);

            moveWheels("wheel_right_front",  0, moveToExecute);
            moveWheels("wheel_right_back",  0, moveToExecute);                
        }
        else if(moveToExecute == "move_butter")
        {
            sendPosition("shoulder_left",2.6);
            sendPosition("shoulder_right",0.39);

            sendPosition("elbow_left",1.5);
            sendPosition("elbow_right",-1.5);

            sendPosition("hand_left",-1.3);
            sendPosition("hand_right",-1.3);

        }
        else if(moveToExecute == "init_position")
        {
            sendPosition("body",0.174);

            sendPosition("shoulder_left",3);
            sendPosition("shoulder_right",0);

            sendPosition("elbow_left",0);
            sendPosition("elbow_right",0);

            sendPosition("hand_left",0);
            sendPosition("hand_right",0);
        }
        
        return;
    }

    void testMode(){
        char input;
        while(input != 'k')
        {
            std::cin >> input;

            switch(input)
            {
                case 'w':
                    execMove("move_forward");
                    break;

                case 's':
                    execMove("walk_back");
                    break;

                case 'a':
                    execMove("rotate_counterclockwise");
                    break;

                case 'd':
                    execMove("rotate_clockwise");
                    break;

                case 'p':
                    execMove("move_butter");
                    break;

                case 'i':
                    execMove("init_position");
                    break;
                    
                default:
                    break;
            }  
        }
    }
};

#endif