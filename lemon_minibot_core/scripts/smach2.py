#!/usr/bin/env python  

import sys, select, termios, tty
import rospy
import math
import tf
import roslib
roslib.load_manifest("rosparam")
import rosparam
import time
import os
import rospkg

import geometry_msgs.msg
import turtlesim.srv

#get pkg dir & get to param
rospack = rospkg.RosPack()
dirpath = rospack.get_path('lemon_minibot_core')
os.chdir(dirpath+'/param')


class artag_server:
    def __init__(self):
        ########### load yaml file ###########
        try:
            self.data = rosparam.load_file("smach.yaml",default_namespace="smach")

            print "load yaml file success"
            #update to server
            for params, ns in self.data:
                rosparam.upload_params(ns,params)
            time.sleep(0.5)
        except:
            print "load yaml file faile"
            sys.exit(0)
        ########### load param ###########
        try:
            self.slam = int(rospy.get_param('~/smach/slam'))
            self.navigation = float(rospy.get_param('~/smach/navigation'))
            self.control = float(rospy.get_param('~/smach/control'))

            print "load param success"
            time.sleep(0.5)
            print "**********************************************"
            print "value:"
            print ("slam {  %d  }" % (self.slam))
            print ("navigation {  %d  }" % (self.navigation))
            print ("control {  %d  }" % (self.control))
            print "**********************************************"
            time.sleep(0.5)
        except:
            print "load param faile"
            sys.exit(0)

    def dump(self):
        rosparam.dump_params("smach.yaml","smach")
        print "yaml file saved"

    def save2Server(self):
        rospy.set_param('~/smach/slam',self.local1_con)
        rospy.set_param('~/smach/navigation',self.local1_x)
        rospy.set_param('~/smach/control',self.local1_y)

        
        print "**********************************************"
        print "value:"
        print ("slam {  %d  }" % (self.slam))
        print ("navigation {  %d  }" % (self.navigation))
        print ("control {  %d  }" % (self.control))
        print "**********************************************"


    def update(self):

        ##############################################
        

        time.sleep(0.5)




if __name__ == '__main__':
    rospy.init_node('alexa_assistant')
    up = artag_server()
    while True:
        if not rospy.is_shutdown():
            up.update()
            up.save2Server()
        else:
            up.dump()
            print "Shutting down"
            sys.exit(0)
