#include "ros/ros.h"
#include "robot_moves/Behav_mov.h"

int main(int argc, char **argv)
{
  int count = 0;
  robot_moves::Behav_mov msg;
  char opc = ' ';

  ros::init(argc, argv, "behaviour_topic_sim");
  ros::NodeHandle n;
  
  ros::Publisher simPub = n.advertise<robot_moves::Behav_mov>("behaviour_movimento", 10);
  ros::Rate loop_rate(10);

  while (opc != 'k')
  { 
    std::cin >> opc;
    switch(opc){
      case 'w':
        msg.move = "move_forward";
        break;
      case 's':
        msg.move = "walk_back";
        break;
      case 'd':
        msg.move = "rotate_counterclockwise";
        break;
      case 'a':
        msg.move = "rotate_clockwise";
        break;
      case 'p':
        msg.move = "move_butter";
        break;
      case 'i':
        msg.move = "init_position";
        break;
      default:
        break;
    }

    simPub.publish(msg); 
  }

  ros::spin();
  return 0;
}