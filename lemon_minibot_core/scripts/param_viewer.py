#!/usr/bin/env python

import sys, select, termios, tty
import rospy
import math
import tf
import roslib
roslib.load_manifest("rosparam")
import rosparam
import os
import rospkg
######


def init():
    try:
        slam = int(rospy.get_param('~/smach/slam'))
        navigation = int(rospy.get_param('~/smach/navigation'))
        control = int(rospy.get_param('~/smach/control'))

        local1_con = int(rospy.get_param('~/artag/location1/Confidence'))
        local1_x = float(rospy.get_param('~/artag/location1/x'))
        local1_y = float(rospy.get_param('~/artag/location1/y'))

        local2_con = int(rospy.get_param('~/artag/location2/Confidence'))
        local2_x = float(rospy.get_param('~/artag/location2/x'))
        local2_y = float(rospy.get_param('~/artag/location2/y'))

        local3_con = int(rospy.get_param('~/artag/location3/Confidence'))
        local3_x = float(rospy.get_param('~/artag/location3/x'))
        local3_y = float(rospy.get_param('~/artag/location3/y'))

        local4_con = int(rospy.get_param('~/artag/location4/Confidence'))
        local4_x = float(rospy.get_param('~/artag/location4/x'))
        local4_y = float(rospy.get_param('~/artag/location4/y'))
        
        #print "load param success"
        time.sleep(0.5)
        print "**********************************************"
        print "value:"
        print ("local1 { con %d , x %.4f , y %.4f }" % (self.local1_con,self.local1_x,self.local1_y))
        print ("local2 { con %d , x %.4f , y %.4f }" % (self.local2_con,self.local2_x,self.local2_y))
        print ("local3 { con %d , x %.4f , y %.4f }" % (self.local3_con,self.local3_x,self.local3_y))
        print ("local4 { con %d , x %.4f , y %.4f }" % (self.local4_con,self.local4_x,self.local4_y))
        print "**********************************************"
        print "**********************************************"
        print "value:"
        print ("slam       {  %d  }" % (slam))        #0:none, 1:open
        print ("navigation {  %d  }" % (navigation))  #0:none, 1:location1, 2:location2 ,etc
        print ("control    {  %d  }" % (control))     #0:none, 1:front, 2:back, 3:left, 2:right
        print "**********************************************"
    except:
        print "load param faile"
        sys.exit(0)


if __name__ == '__main__':
    rospy.init_node('param_viewer')
    while True:
        if not rospy.is_shutdown():
            init()
        else:
            print "Shutting down"
            sys.exit(0)
