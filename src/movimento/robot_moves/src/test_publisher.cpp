#include "ros/ros.h"
#include "std_msgs/String.h"

int main(int argc, char **argv)
{
  int count = 0;
  std_msgs::String msg;
  ros::init(argc, argv, "behaviour_topic_sim");
  ros::NodeHandle n;
  
  ros::Publisher chatter_pub = n.advertise<std_msgs::String>("behaviour_movimento", 1000);
  ros::Rate loop_rate(1);

  msg.data = "move_butter";

  while (ros::ok())
  {
    chatter_pub.publish(msg);
    if(count>1000000)msg.data = "move_forward";
    count++;
    ros::spinOnce();
  }

  return 0;
}