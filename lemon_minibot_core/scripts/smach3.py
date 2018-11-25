#!/usr/bin/python

from flask import Flask 
from flask_ask import Ask , statement , question , session

import json
import requests
import time
import unidecode
######
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

#get pkg dir & get to param
rospack = rospkg.RosPack()
dirpath = rospack.get_path('lemon_minibot_core')
os.chdir(dirpath+'/param')

#define app to alexa skill kit
app = Flask(__name__)
ask = Ask(app, "/minibot_controller")

slam = 0
navugation = 0
control = 0


def init():
    try:
        data = rosparam.load_file("smach.yaml",default_namespace="smach")
        print "load yaml file success"
        #update to server
        for params, ns in data:
            rosparam.upload_params(ns,params)
        time.sleep(0.5)
    except:
        print "load yaml file faile"
        sys.exit(0)
    
    try:
        slam = int(rospy.get_param('~/smach/slam'))
        navigation = float(rospy.get_param('~/smach/navigation'))
        control = float(rospy.get_param('~/smach/control'))

        print "load param success"
        time.sleep(0.5)
        print "**********************************************"
        print "value:"
        print ("slam       {  %d  }" % (slam))        #0:none, 1:open
        print ("navigation {  %d  }" % (navigation))  #0:none, 1:location1, 2:location2 ,etc
        print ("control    {  %d  }" % (control))     #0:none, 1:front, 2:back, 3:left, 2:right
        print "**********************************************"
        time.sleep(0.1)
    except:
        print "load param faile"
        sys.exit(0)




@ask.launch
def launch():
    speech_text = 'Welcome to the lemon minibot, I am your personal guiding robot'
    return question(speech_text)

@ask.intent('help')
def hello_world():
    speech_text = 'If you would like to control me, just say go and command, like, Go forward, or Go backward, or go left, or go right'
    return question(speech_text)

###############################################
@ask.intent('slam')
def hello_world():
    speech_text = 'I am so exciting! Lest go mapping!'
    rospy.set_param('~/smach/slam','1')
    return question(speech_text)


###############################################


@ask.intent('hello',convert={'Name': 'name'})
def hello(Name):
    return question('Hello {}'.format(Name))

@ask.intent('HelloIntent',convert={'Name': 'name'})
def hello(Name):
    return question('Hello {}'.format(Name))

@ask.intent('action')
def hello_world():
    speech_text = 'move me'
    return question(speech_text)


@ask.intent('')
def help():
    speech_text = 'You can say hello to me!'
    return question(speech_text).reprompt(speech_text).simple_card('HelloWorld', speech_text)


@ask.session_ended
def session_ended():
    return "{}", 200


def reloadp():
    data = rosparam.load_file("location.yaml",default_namespace="smach")
    #update to server
    for params, ns in data:
        rosparam.upload_params(ns,params)

def dump():
    rosparam.dump_params("smach.yaml","smach")



if __name__ == '__main__':
    while True:
        if not rospy.is_shutdown():
            app.run(debug=True)
            dump()
            reloadp()
            
        else:
            dump()
            print "yaml file saved"
            print "Shutting down"
            sys.exit(0)
    
