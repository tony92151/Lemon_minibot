#!/usr/bin/python

import rospy
import time
import sys
import math
import string
import yaml 
import os


# get local dir
curPath = os.path.dirname(os.path.realpath(__file__))
# get yaml dir & yaml file's name
yamlPath = os.path.join(curPath, "param/smach.yaml")

f = open(yamlPath, 'r', encoding='utf-8')
cfg = f.read()

d = yaml.load(cfg)




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

