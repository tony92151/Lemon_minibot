#!/usr/bin/env python  

import sys, select, termios, tty
import rospy
import math
import tf
import roslib
roslib.load_manifest("rosparam")
import rosparam
import time

import geometry_msgs.msg
import turtlesim.srv

class artag_server:
    def __init__(self):
        ########### load yaml file ###########
        try:
            self.data = rosparam.load_file("test.yaml",default_namespace="artag")
            print "load yaml file success"
            #update to server
            for params, ns in self.data:
                rosparam.upload_params(ns,params)
            time.sleep(1)
        except:
            print "load yaml file faile"
            sys.exit(0)
        ########### load param ###########
        try:
            self.local1_con = int(rospy.get_param('~/artag/location1/Confidence'))
            self.local1_x = float(rospy.get_param('~/artag/location1/x'))
            self.local1_y = float(rospy.get_param('~/artag/location1/y'))

            self.local2_con = int(rospy.get_param('~/artag/location2/Confidence', '0'))
            self.local2_x = float(rospy.get_param('~/artag/location2/x', '0'))
            self.local2_y = float(rospy.get_param('~/artag/location2/y', '0'))

            self.local3_con = int(rospy.get_param('~/artag/location3/Confidence', '0'))
            self.local3_x = float(rospy.get_param('~/artag/location3/x', '0'))
            self.local3_y = float(rospy.get_param('~/artag/location3/y', '0'))
            print "load param success"
            time.sleep(1)
            print "value:"
            print "**********************************************"
            print ("local1 { con %d , x %.4f , y %.4f }" % (self.local1_con,self.local1_x,self.local1_y))
            print ("local2 { con %d , x %.4f , y %.4f }" % (self.local2_con,self.local2_x,self.local2_y))
            print ("local3 { con %d , x %.4f , y %.4f }" % (self.local3_con,self.local3_x,self.local3_y))
            print "**********************************************"
            time.sleep(1)
        except:
            print "load param faile"
            sys.exit(0)

    def dump(self):
        rosparam.dump_params("test.yaml","artag")
        print "yaml file saved"

    def save2Server(self):
        rospy.set_param('~/artag/location1/Confidence',self.local1_con)
        rospy.set_param('~/artag/location1/x',self.local1_x)
        rospy.set_param('~/artag/location1/y',self.local1_y)

        rospy.set_param('~/artag/location2/Confidence',self.local2_con)
        rospy.set_param('~/artag/location2/x',self.local2_x)
        rospy.set_param('~/artag/location2/y',self.local2_y)

        rospy.set_param('~/artag/location3/Confidence',self.local3_con)
        rospy.set_param('~/artag/location3/x',self.local3_x)
        rospy.set_param('~/artag/location3/y',self.local3_y)

        print "value:"
        print "**********************************************"
        print ("local1 { con %d , x %.4f , y %.4f }" % (self.local1_con,self.local1_x,self.local1_y))
        print ("local2 { con %d , x %.4f , y %.4f }" % (self.local2_con,self.local2_x,self.local2_y))
        print ("local3 { con %d , x %.4f , y %.4f }" % (self.local3_con,self.local3_x,self.local3_y))
        print "**********************************************"


    def update(self):

        ##############################################
        if not self.local1_con:
            listener = tf.TransformListener()
            try:
                (trans,rot) = listener.lookupTransform('/odom', '/base_footprint', rospy.Time(0))
                trans[0] = round(trans[0],2)
                trans[1] = round(trans[1],2)
                print("find local 1 x: %f , y: %f " % (trans[0],trans[1]))
                self.local1_x = trans[0]
                self.local1_y = trans[1]
                self.local1_con = 100
                print("save local 1 to param server ")
            except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
                self.local1_con = 0
                print "local 1 not finded"
        else:
            print "Local 1 finded"
        
        ##############################################
        if not self.local2_con:
            listener2 = tf.TransformListener()
            try:
                (trans,rot) = listener2.lookupTransform('/odom', '/base_footprint', rospy.Time(0))
                trans[0] = round(trans[0],2)
                trans[1] = round(trans[1],2)
                print("find local 2 x: %f , y: %f " % (trans[0],trans[1]))
                self.local2_x = trans[0]
                self.local2_y = trans[1]
                self.local2_con = 100
                print("save local 2 to param server ")

            except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
                self.local2_con = 0
                print "local 2 not finded"

            for params, ns in self.data:
                rosparam.upload_params(ns,params)
        else:
            print "Local 2 finded"

        ##############################################
        if not self.local3_con:
            listener3 = tf.TransformListener()
            try:
                (trans,rot) = listener3.lookupTransform('/odom', '/base_footprint', rospy.Time(0))
                trans[0] = round(trans[0],2)
                trans[1] = round(trans[1],2)
                print("find local 3 x: %f , y: %f " % (trans[0],trans[1]))
                self.local3_x = trans[0]
                self.local3_y = trans[1]
                self.local3_con = 100
                print("save local 3 to param server ")

            except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
                self.local3_con = 0
                print "local 3 not finded"

            for params, ns in self.data:
                rosparam.upload_params(ns,params)
        else:
            print "Local 3 finded"
        time.sleep(0.5)




if __name__ == '__main__':
    rospy.init_node('tf_listener')
    up = artag_server()
    while True:
        if not rospy.is_shutdown():
            up.update()
            up.save2Server()
        else:
            up.dump()
            print "Shutting down"
            sys.exit(0)
