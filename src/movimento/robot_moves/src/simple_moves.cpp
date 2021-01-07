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
        bool moveMotor(std::string motor){
            gpositionClient = nh.serviceClient<robot_moves::get_float>(robotName+"/"+motor+"/get_target_position");

            return gpositionClient.call(getFloat);
        }

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
};

int main(int argc, char **argv){
    ros::init(argc, argv, "movementSimple_moves");
    robotControl *controller = new robotControl();

    std::string motorReq = "braco_esq";

    std::cout << controller->robotName << std::endl;
//    std::cout << "Motor desejado: ";
//    std::cin >> motorReq;

    std::cout << "A posição atual de " << motorReq << " requisitado eh: " << controller->moveMotor(motorReq) << std::endl;

    return 0;
}