cmake_minimum_required(VERSION 2.8.3)

project(butter_robot_v2)

find_package(catkin REQUIRED COMPONENTS
	roscpp
	rospy
	std_msgs
	message_generation)

catkin_package(
	CATKIN_DEPENDS message_runtime)

find_package(roslaunch)

foreach(dir config launch meshes urdf)
	install(DIRECTORY ${dir}/
		DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/${dir})
endforeach(dir)

add_message_files(
  FILES
  visparabeh.msg
)

generate_messages(
  DEPENDENCIES
  std_msgs
)
