#!/usr/bin/python

#reference http://wiki.ros.org/roslaunch/API%20Usage

import roslaunch
import rospy
import rospkg

#get pkg dir & get to param
rospack = rospkg.RosPack()
dirpath = rospack.get_path('turtlebot3_copy')

rospy.init_node('Core_controller', anonymous=False)
uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
roslaunch.configure_logging(uuid)

slam_launch = roslaunch.parent.ROSLaunchParent(uuid, [dirpath+"/launch/turtlebot_world2.launch"])


slam_launch.start()
rospy.loginfo("started")

rospy.sleep(15)
# 3 seconds later
slam_launch.shutdown()