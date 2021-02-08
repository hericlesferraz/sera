#include "ros/ros.h"
#include "std_msgs/String.h"

#include "robot_moves/set_float.h"
#include "robot_moves/get_float.h"

class robotControl{
    private:
        ros::NodeHandle nh;
        robot_moves::set_float sendRequisitionFloat;
        robot_moves::get_float getFloat;

        ros::ServiceClient gpositionClient, positionClient, velocityClient;

        //Funções para comunicação com o simulador
        void getNameCallback(const std_msgs::String::ConstPtr &model){
            robotName = model->data.c_str();
            return;
        }

        bool sendPosition(std::string motor, float requisition){
            sendRequisitionFloat.request.value = requisition;
            positionClient = nh.serviceClient<robot_moves::set_float>(robotName+"/"+motor+"/set_position");

            return positionClient.call(sendRequisitionFloat);
        }

    public:
        std::string robotName = " ";

        //Construtor para inicializar o objeto e receber o nome aleatório do robô
        robotControl(){
            ros::Subscriber getName = nh.subscribe("model_name", 100, &robotControl::getNameCallback, this);
            while(robotName == " "){
                ros::spinOnce();
            }
            getName.shutdown();

            getFloat.request.ask = false;
        }

        //Funções para o usuário
        bool moveMotor(std::string motor, bool request){
            gpositionClient = nh.serviceClient<robot_moves::get_float>("/"+robotName+"/"+motor+"/get_target_position");
            gpositionClient.call(getFloat);

            getFloat.response.value += (request) ? 3.14 : -3.14;
            return sendPosition(motor , getFloat.response.value);
        }
};

int main(int argc, char **argv){
    ros::init(argc, argv, "movementSimple_moves");
    robotControl *controller = new robotControl();

    std::string motorReq;
    char opc=' ';

    do{
        std::cin >> opc;
        switch(opc){
            case 'w':
                motorReq = "wheel_left_front";
                controller->moveMotor(motorReq,1);
                motorReq = "wheel_left_back";
                controller->moveMotor(motorReq,0);

                motorReq = "wheel_right_front";
                controller->moveMotor(motorReq,0);
                motorReq = "wheel_right_back";
                controller->moveMotor(motorReq,0);
                break;
            case 's':
                motorReq = "wheel_left_front";
                controller->moveMotor(motorReq,0);
                motorReq = "wheel_left_back";
                controller->moveMotor(motorReq,1);

                motorReq = "wheel_right_front";
                controller->moveMotor(motorReq,1);
                motorReq = "wheel_right_back";
                controller->moveMotor(motorReq,1);
                break;
            default:
                break;
        }

    }while(opc != 27);

    return 0;
}