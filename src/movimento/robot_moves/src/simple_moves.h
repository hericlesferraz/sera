#ifndef SIMPLE_MOVES_H
#define SIMPLE_MOVES_H
#include <map>
#include <utility>

#include "ros/ros.h"
#include "std_msgs/String.h"

#include "robot_moves/set_float.h"
#include "robot_moves/get_float.h"

#include "robot_moves/Behav_mov.h"

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

            getFloat.response.value += (request) ? 0.628 : -0.628;
            return sendPosition(motor , getFloat.response.value);
        }

        void moveWheels(std::string movement){
            if(movement == "move_forward"){
                motorReq = "wheel_left_front";
                moveMotor(motorReq,1);
                motorReq = "wheel_left_back";
                moveMotor(motorReq,1);

                motorReq = "wheel_right_front";
                moveMotor(motorReq,0);
                motorReq = "wheel_right_back";
                moveMotor(motorReq,0);                
            }
            if(movement == "walk_back"){
                motorReq = "wheel_left_front";
                moveMotor(motorReq,0);
                motorReq = "wheel_left_back";
                moveMotor(motorReq,0);

                motorReq = "wheel_right_front";
                moveMotor(motorReq,1);
                motorReq = "wheel_right_back";
                moveMotor(motorReq,1);                
            }
            if(movement == "rotate_clockwise"){
                motorReq = "wheel_left_front";
                moveMotor(motorReq,1);
                motorReq = "wheel_left_back";
                moveMotor(motorReq,1);

                motorReq = "wheel_right_front";
                moveMotor(motorReq,1);
                motorReq = "wheel_right_back";
                moveMotor(motorReq,1);                
            }
            if(movement == "rotate_counterclockwise"){
                motorReq = "wheel_left_front";
                moveMotor(motorReq,0);
                motorReq = "wheel_left_back";
                moveMotor(motorReq,0);

                motorReq = "wheel_right_front";
                moveMotor(motorReq,0);
                motorReq = "wheel_right_back";
                moveMotor(motorReq,0);                
            }
            return;
        }

        void pageExecution(std::string){
            
            return;
        }
        
};


#endif