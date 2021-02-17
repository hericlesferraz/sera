#include "ros/ros.h"
#include "std_msgs/String.h"

#include "robot_moves/set_float.h"
#include "robot_moves/get_float.h"

#include "robot_moves/Behav_mov.h"

class robotControl{
    private:
        ros::NodeHandle nh;
        ros::ServiceClient gpositionClient, positionClient, velocityClient;
        ros::Subscriber behav2Mov;

        robot_moves::set_float sendRequisitionFloat;
        robot_moves::get_float getFloat;

        std::string motorReq;

        //Funções para comunicação com o simulador
        void getNameCallback(const std_msgs::String::ConstPtr &model){
            robotName = model->data.c_str();
            return;
        }

        void behav2MovCallback(const std_msgs::String::ConstPtr &req){
            switch(req->move){
                case "move_forward":
                    motorReq = "wheel_left_front";
                    moveMotor(motorReq,1);
                    motorReq = "wheel_left_back";
                    moveMotor(motorReq,1);

                    motorReq = "wheel_right_front";
                    moveMotor(motorReq,0);
                    motorReq = "wheel_right_back";
                    moveMotor(motorReq,0);
                    break;

                case "walk_back":
                    motorReq = "wheel_left_front";
                    moveMotor(motorReq,0);
                    motorReq = "wheel_left_back";
                    moveMotor(motorReq,0);

                    motorReq = "wheel_right_front";
                    moveMotor(motorReq,1);
                    motorReq = "wheel_right_back";
                    moveMotor(motorReq,1);
                    break;

                case "rotate_clockwise":
                    motorReq = "wheel_left_front";
                    moveMotor(motorReq,1);
                    motorReq = "wheel_left_back";
                    moveMotor(motorReq,1);

                    motorReq = "wheel_right_front";
                    moveMotor(motorReq,1);
                    motorReq = "wheel_right_back";
                    moveMotor(motorReq,1);
                    break;

                case "rotate_counterclockwise":
                    motorReq = "wheel_left_front";
                    moveMotor(motorReq,0);
                    motorReq = "wheel_left_back";
                    moveMotor(motorReq,0);

                    motorReq = "wheel_right_front";
                    moveMotor(motorReq,0);
                    motorReq = "wheel_right_back";
                    moveMotor(motorReq,0);
                    break;
                
                case "page_catchbutter":
                    break;
                
                default:
                    break;
            }

        }

        bool sendPosition(std::string motor, float requisition){
            sendRequisitionFloat.request.value = requisition;
            positionClient = nh.serviceClient<robot_moves::set_float>(robotName+"/"+motor+"/set_position");

            return positionClient.call(sendRequisitionFloat);
        }

    public:
        std::string robotName = " ";

        //Construtor para inicializar o objeto, receber o nome aleatório do robô e iniciar comunicação com o Behavior
        robotControl(){
            ros::Subscriber getName = nh.subscribe("model_name", 100, &robotControl::getNameCallback, this);
            while(robotName == " "){
                ros::spinOnce();
            }
            getName.shutdown();

            getFloat.request.ask = false;

            behav2Mov = nh.subscribe("behaviour_movimento", 100, &robotControl::behav2MovCallback, this);
        }

        //Funções para o usuário
        bool moveMotor(std::string motor, bool request){
            gpositionClient = nh.serviceClient<robot_moves::get_float>("/"+robotName+"/"+motor+"/get_target_position");
            gpositionClient.call(getFloat);

            getFloat.response.value += (request) ? 0.628 : -0.628;
            return sendPosition(motor , getFloat.response.value);
        }
};

int main(int argc, char **argv){
    ros::init(argc, argv, "movementSimple_moves");
    robotControl *controller = new robotControl();

    ros::spin();

    return 0;
}