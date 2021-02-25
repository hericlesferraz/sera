cmake_minimum_required(VERSION 3.0.2)
project(robot_moves)

find_package(catkin REQUIRED COMPONENTS roscpp std_msgs message_generation)

################################################
## Declare ROS messages, services and actions ##
################################################

## Generate messages in the 'msg' folder
add_message_files(
   FILES
   Behav_mov.msg
)

## Generate services in the 'srv' folder
add_service_files(
    FILES
    set_float.srv
    get_float.srv
)

## Generate actions in the 'action' folder
# add_action_files(
#   FILES
#   Action1.action
#   Action2.action
# )

## Generate added messages and services with any dependencies listed here
 generate_messages(
   DEPENDENCIES
   std_msgs
 )

################################################
## Declare ROS dynamic reconfigure parameters ##
################################################


###################################
## catkin specific configuration ##
###################################

catkin_package(
# INCLUDE_DIRS include
#  LIBRARIES robot_moves
   CATKIN_DEPENDS roscpp std_msgs message_runtime
#  DEPENDS system_lib
)

###########
## Build ##
###########

## Specify additional locations of header files
## Your package locations should be listed before other locations
include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)

add_executable(simple_moves src/simple_moves.cpp)
add_dependencies(simple_moves robot_moves_generate_messages_cpp)
target_link_libraries(simple_moves ${catkin_LIBRARIES})

add_executable(test_publisher  src/test_publisher.cpp)
add_dependencies(test_publisher  robot_moves_generate_messages_cpp)
target_link_libraries(test_publisher  ${catkin_LIBRARIES})

#############
## Install ##
#############
