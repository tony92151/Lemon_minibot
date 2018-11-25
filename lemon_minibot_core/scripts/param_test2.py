#!/usr/bin/env python  
import rospy
import math
import tf
import geometry_msgs.msg
import turtlesim.srv


def update():
    listener = tf.TransformListener()


    while not rospy.is_shutdown():
        try:
            (trans,rot) = listener.lookupTransform('/odom', '/base_footprint', rospy.Time(0))
            trans[0] = round(trans[0],2)
            trans[1] = round(trans[1],2)
            print("local x: %f , y: %f " % (trans[0],trans[1]))
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue







if __name__ == '__main__':
    rospy.init_node('tf_listener')
    update()
    