#!/usr/bin/python

import rospy
import time
import sys
import math
import string


rospy.init_node('smash', anonymous=True)
sm = smash()
rospy.spin()
loca1_con = rospy.get_param('~/ar/location1/Confidence', 0)
sloca_x = rospy.get_param('~/ar/location1/x', 0)

for x in range(0, 50):
    print loca_x
    time.sleep(0.01)
rospy.set_param('~/ar/location1/x', 100)
for x in range(0, 50):
    print loca_x
    time.sleep(0.01)

