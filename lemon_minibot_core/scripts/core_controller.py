#!/usr/bin/python

#reference http://wiki.ros.org/roslaunch/API%20Usage

import roslaunch
import rospy
import rospkg

#get pkg dir & get to param
rospack = rospkg.RosPack()

dirpath_ar = rospack.get_path('lemon_minibot_detect')
dirpath_core = rospack.get_path('lemon_minibot_core')
dirpath_rviz = rospack.get_path('minibot_simulation')

dirpath_nav = rospack.get_path('turtlebot3_copy')

class core_control:
    def __init__(self):
        uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
        roslaunch.configure_logging(uuid)
        
        self.mapping_launch = roslaunch.parent.ROSLaunchParent(uuid, [dirpath_core+"/launch/lemon_minibot_gmapping.launch"])
        self.mapping_launch_already = 0

        self.nav_launch = roslaunch.parent.ROSLaunchParent(uuid, [dirpath_core+"/launch/lemon_minibot_navigation.launch"])
        self.nav_launch_already = 0

    def init_again(self):
        uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
        roslaunch.configure_logging(uuid)
        self.mapping_launch = roslaunch.parent.ROSLaunchParent(uuid, [dirpath_core+"/launch/lemon_minibot_gmapping.launch"])
        self.nav_launch = roslaunch.parent.ROSLaunchParent(uuid, [dirpath_core+"/launch/lemon_minibot_navigation.launch"])

    def update(self):
        if rospy.get_param('~/smach/slam')==1:
            #rospy.sleep(0.5)
            if self.mapping_launch_already == 0:
                rospy.sleep(1)
                self.mapping_launch.start()
                self.mapping_launch_already = 1
                rospy.loginfo("slam started")
            else:
                rospy.loginfo("slam have already launched")
                rospy.sleep(0.3)

        else:
            if self.mapping_launch_already == 1:
                rospy.sleep(0.3)
                self.mapping_launch.shutdown()
                self.mapping_launch_already = 0
                self.init_again()
                rospy.loginfo("slam closed")
            else:
                rospy.loginfo("slam have already closed")
                rospy.sleep(1)

        #######################################
        if rospy.get_param('~/smach/navigation')!=-1:
            #rospy.sleep(0.5)
            if self.nav_launch_already == 0:
                rospy.sleep(1)
                self.nav_launch.start()
                self.nav_launch_already = 1
                rospy.loginfo("navigation started")
            else:
                rospy.loginfo("navigation have already launched")
                rospy.sleep(0.3)

        else :
            if self.nav_launch_already == 1:
                rospy.sleep(0.3)
                self.nav_launch.shutdown()
                self.nav_launch_already = -1
                self.init_again()
                rospy.loginfo("navigation closed")
            else:
                rospy.loginfo("navigation have already closed")
                rospy.sleep(1)
        

if __name__ == '__main__':
    rospy.init_node('Core_controller', anonymous=False)
    core = core_control()
    while True:
        if not rospy.is_shutdown():
            core.update()
        else:
            print "Shutting down"
            sys.exit(0)
