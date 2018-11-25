#!/usr/bin/python

import rospy
from std_msgs.msg import String
import time
import sys, select, termios, tty
import tf
import math
import string
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

import turtlesim.msg

def tf_bro():
    rate = rospy.Rate(10) # 10hz
    br = tf.TransformBroadcaster()
    bt.sendTransform((msg.x, msg.y, 0),
                        tf.transformations.quaternion_from_euler(0, 0, msg.theta),
                        rospy.Time.now(),
                        turtlename,
                        "world")
    hello_str = "hello world %s" % rospy.get_time()
    rospy.loginfo(hello_str)
    pub.publish(hello_str)
    rate.sleep()

if __name__ == '__main__':

    rospy.init_node('pointer_tf_broadcaster')
    try:
        tf_bro()
    except rospy.ROSInterruptException:
        pass


