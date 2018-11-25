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
            self.data = rosparam.load_file("location.yaml",default_namespace="artag")
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
            self.local1_con = int(rospy.get_param('~/artag/location1/Confidence'))
            self.local1_x = float(rospy.get_param('~/artag/location1/x'))
            self.local1_y = float(rospy.get_param('~/artag/location1/y'))

            self.local2_con = int(rospy.get_param('~/artag/location2/Confidence'))
            self.local2_x = float(rospy.get_param('~/artag/location2/x'))
            self.local2_y = float(rospy.get_param('~/artag/location2/y'))

            self.local3_con = int(rospy.get_param('~/artag/location3/Confidence'))
            self.local3_x = float(rospy.get_param('~/artag/location3/x'))
            self.local3_y = float(rospy.get_param('~/artag/location3/y'))

            self.local4_con = int(rospy.get_param('~/artag/location4/Confidence'))
            self.local4_x = float(rospy.get_param('~/artag/location4/x'))
            self.local4_y = float(rospy.get_param('~/artag/location4/y'))
            print "load param success"
            time.sleep(0.5)
            print "**********************************************"
            print "value:"
            print ("local1 { con %d , x %.4f , y %.4f }" % (self.local1_con,self.local1_x,self.local1_y))
            print ("local2 { con %d , x %.4f , y %.4f }" % (self.local2_con,self.local2_x,self.local2_y))
            print ("local3 { con %d , x %.4f , y %.4f }" % (self.local3_con,self.local3_x,self.local3_y))
            print ("local4 { con %d , x %.4f , y %.4f }" % (self.local4_con,self.local4_x,self.local4_y))
            print "**********************************************"
            time.sleep(0.5)
        except:
            print "load param faile"
            sys.exit(0)

        self.listener = tf.TransformListener()
        self.listener2 = tf.TransformListener()
        self.listener3 = tf.TransformListener()
        self.listener4 = tf.TransformListener()

    def reload(self):
        self.data = rosparam.load_file("location.yaml",default_namespace="artag")
        #update to server
        for params, ns in self.data:
            rosparam.upload_params(ns,params)

    def dump(self):
        rosparam.dump_params("location.yaml","artag")
        

    def save2Server(self):
        rospy.set_param('/artag/location1/Confidence',self.local1_con)
        rospy.set_param('/artag/location1/x',self.local1_x)
        rospy.set_param('/artag/location1/y',self.local1_y)

        rospy.set_param('/artag/location2/Confidence',self.local2_con)
        rospy.set_param('/artag/location2/x',self.local2_x)
        rospy.set_param('/artag/location2/y',self.local2_y)

        rospy.set_param('/artag/location3/Confidence',self.local3_con)
        rospy.set_param('/artag/location3/x',self.local3_x)
        rospy.set_param('/artag/location3/y',self.local3_y)

        rospy.set_param('/artag/location4/Confidence',self.local4_con)
        rospy.set_param('/artag/location4/x',self.local4_x)
        rospy.set_param('/artag/location4/y',self.local4_y)

        

        print "**********************************************"
        print "value:"
        print ("local1 { con %d , x %.4f , y %.4f }" % (self.local1_con,self.local1_x,self.local1_y))
        print ("local2 { con %d , x %.4f , y %.4f }" % (self.local2_con,self.local2_x,self.local2_y))
        print ("local3 { con %d , x %.4f , y %.4f }" % (self.local3_con,self.local3_x,self.local3_y))
        print ("local4 { con %d , x %.4f , y %.4f }" % (self.local4_con,self.local4_x,self.local4_y))
        print "**********************************************"


    def update(self):

        ##############################################
        try:
            (trans,rot) = self.listener.lookupTransform('/odom', '/ar_marker_0', rospy.Time(0))
            trans[0] = round(trans[0],2)
            trans[1] = round(trans[1],2)
            print("find local 1 x: %f , y: %f " % (trans[0],trans[1]))
            self.local1_x = trans[0]
            self.local1_y = trans[1]
            self.local1_con = 100

        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            print "local 1 not finded"
        
        ##############################################

        try:
            (trans,rot) = self.listener2.lookupTransform('/odom', '/ar_marker_1', rospy.Time(0))
            trans[0] = round(trans[0],2)
            trans[1] = round(trans[1],2)
            print("find local 2 x: %f , y: %f " % (trans[0],trans[1]))
            self.local2_x = trans[0]
            self.local2_y = trans[1]
            self.local2_con = 100

        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            print "local 2 not finded"



        ##############################################

        try:
            (trans,rot) = self.listener3.lookupTransform('/odom', '/ar_marker_2', rospy.Time(0))
            trans[0] = round(trans[0],2)
            trans[1] = round(trans[1],2)
            print("find local 3 x: %f , y: %f " % (trans[0],trans[1]))
            self.local3_x = trans[0]
            self.local3_y = trans[1]
            self.local3_con = 100

        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            print "local 3 not finded"


        ##############################################

        try:
            (trans,rot) = self.listener4.lookupTransform('/odom', '/ar_marker_3', rospy.Time(0))
            trans[0] = round(trans[0],2)
            trans[1] = round(trans[1],2)
            print("find local 4 x: %f , y: %f " % (trans[0],trans[1]))
            self.local3_x = trans[0]
            self.local3_y = trans[1]
            self.local3_con = 100

        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            print "local 4 not finded"

        for params, ns in self.data:
            rosparam.upload_params(ns,params)

        time.sleep(0.1)




if __name__ == '__main__':
    rospy.init_node('tf_listener')
    up = artag_server()
    while True:
        if not rospy.is_shutdown():
            up.update()
            up.save2Server()
            up.dump()
            up.reload()

        else:
            up.dump()
            print "yaml file saved"
            print "Shutting down"
            sys.exit(0)
