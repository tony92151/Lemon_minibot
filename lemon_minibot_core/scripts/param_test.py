#!/usr/bin/env python  
import roslib
roslib.load_manifest('learning_tf')
import rospy
import math
import tf
import geometry_msgs.msg
import turtlesim.srv

if __name__ == '__main__':
    rospy.init_node('tf_listener')

    listener = tf.TransformListener(

    rate = rospy.Rate(10.0)

    try:
        (trans,rot) = listener.lookupTransform('/ar_maker_2', '/odom', rospy.Time(0))
        print("local x: %d , y: %d" % (trans[1],trans[2]))
    except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
        print none
        continue

        rate.sleep()