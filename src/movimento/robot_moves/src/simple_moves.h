#ifndef SIMPLE_MOVES_H
#define SIMPLE_MOVES_H
#include <map>
#include <utility>

#include "ros/ros.h"
#include "std_msgs/String.h"

#include "robot_moves/set_float.h"
#include "robot_moves/get_float.h"

class robotControl{
    private:
        //Variáveis necessárias para o funcionamento geral
        ros::NodeHandle nh;
        ros::ServiceClient gpositionClient, positionClient, velocityClient;
        ros::Subscriber behav2Mov;

        robot_moves::set_float sendRequisitionFloat;
        robot_moves::get_float getFloat;

        std::string robotName = " ";
        std::string motorReq;

        std::map<std::string,int> commandAssociation;
    public:
        //Construtor
        robotControl();

        //Funções apenas prototipadas no header
        void getNameCallback(const std_msgs::String::ConstPtr &model);
        void behav2MovCallback(const std_msgs::String::ConstPtr &req);
        bool sendPosition(std::string motor, float requisition);

        //Funções descritas no header (Descrição de movimentos)
        bool moveMotor(std::string motor, bool request){
            gpositionClient = nh.serviceClient<robot_moves::get_float>("/"+robotName+"/"+motor+"/get_target_position");
            gpositionClient.call(getFloat);

            getFloat.response.value += (request) ? 1.256 : -1.256;
            return sendPosition(motor , getFloat.response.value);
        }

        void moveWheels(std::string movement){
            if(movement == "move_forward"){
                moveMotor("wheel_left_front",1);
                moveMotor("wheel_left_back",1);

                moveMotor("wheel_right_front",0);
                moveMotor("wheel_right_back",0);                
            }
            if(movement == "walk_back"){
                moveMotor("wheel_left_front",0);
                moveMotor("wheel_left_back",0);

                moveMotor("wheel_right_front",1);
                moveMotor("wheel_right_back",1);                
            }
            if(movement == "rotate_clockwise"){
                moveMotor("wheel_left_front",1);
                moveMotor("wheel_left_back",1);

                moveMotor("wheel_right_front",1);
                moveMotor("wheel_right_back",1);                
            }
            if(movement == "rotate_counterclockwise"){
                moveMotor("wheel_left_front",0);
                moveMotor("wheel_left_back",0);

                moveMotor("wheel_right_front",0);
                moveMotor("wheel_right_back",0);                
            }
            return;
        }

        void pageExecution(std::string page){
            if(page == "move_butter"){
                sendPosition("body",0.174);

                sendPosition("shoulder_left",2.6);
                sendPosition("shoulder_right",0.39);

                sendPosition("elbow_left",1.5);
                sendPosition("elbow_right",-1.5);

                sendPosition("hand_left",-1.3);
                sendPosition("hand_right",-1.3);

            }
            if(page == "init_position"){
                sendPosition("body",0);

                sendPosition("shoulder_left",3);
                sendPosition("shoulder_right",0);

                sendPosition("elbow_left",0);
                sendPosition("elbow_right",0);

                sendPosition("hand_left",0);
                sendPosition("hand_right",0);

            }
            return;
        }
        
};


#endif