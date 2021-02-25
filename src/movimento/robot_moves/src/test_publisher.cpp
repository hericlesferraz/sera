#include "ros/ros.h"
#include "std_msgs/String.h"

int main(int argc, char **argv)
{
  int count = 0;
  std_msgs::String msg;
  char opc = ' ';

  ros::init(argc, argv, "behaviour_topic_sim");
  ros::NodeHandle n;
  
  ros::Publisher simPub = n.advertise<std_msgs::String>("behaviour_movimento", 10);
  ros::Rate loop_rate(10);

  while (opc != 'k')
  { 
    std::cin >> opc;
    switch(opc){
      case 'w':
        msg.data = "move_forward";
        break;
      case 's':
        msg.data = "walk_back";
        break;
      case 'd':
        msg.data = "rotate_counterclockwise";
        break;
      case 'a':
        msg.data = "rotate_clockwise";
        break;
      case 'p':
        msg.data = "move_butter";
        break;
      case 'i':
        msg.data = "init_position";
        break;
      default:
        break;
    }

    simPub.publish(msg); 
  }

  ros::spin();
  return 0;
}