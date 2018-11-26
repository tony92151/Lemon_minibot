#!/usr/bin/python

from flask import Flask 
from flask_ask import Ask , statement , question , session

import json
import requests
import time
import unidecode
import random

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
        navigation = int(rospy.get_param('~/smach/navigation'))
        control = int(rospy.get_param('~/smach/control'))

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

@ask.intent('help_intent')
def hello_world():
    speech_text = 'If you would like to control me, just say go and command, like, Go forward, or Go backward, or go left, or go right'
    #speech_text = render_template('win')
    return question(speech_text)

###############################################
@ask.intent('open_slam')
def slam():
    if rospy.get_param('~/smach/slam')!=1:
        speech_text = 'I am so exciting! Lest go mapping!'
        rospy.set_param('~/smach/slam',1)
    else:
        speech_text = 'Mapping are already launched!'
    return question(speech_text)

@ask.intent('close_slam')
def slam():
    if rospy.get_param('~/smach/slam')!=1:
        speech_text = 'Mapping not launched yet!'
    else:
        speech_text = 'OK! the map is saved, go navigation right now'
        #rospy.set_param('~/smach/slam',0)
    
    rospy.set_param('~/smach/slam',0)
    return question(speech_text)

@ask.intent('open_navigation')
def slam():
    if rospy.get_param('~/smach/navigation')!=0:
        speech_text = 'Lest go navigation, tell me any where you want to go!'
        rospy.set_param('~/smach/navigation',0)
    else:
        speech_text = 'navigation are already launched!'
    return question(speech_text)

@ask.intent('close_navigation')
def slam():
    if rospy.get_param('~/smach/navigation')==-1:
        speech_text = 'navigation not launched yet!'
    else:
        speech_text = 'Have a nice day! Goodbye!'
        #rospy.set_param('~/smach/navigation',0)
    
    rospy.set_param('~/smach/navigation',-1)
    return question(speech_text)

@ask.intent('navigation',convert={'navi': str})
def navigation(navi):
    if rospy.get_param('~/smach/navigation')!=-1:
        local =	{
            "bedroom": 1,
            "livingroom": 2,
            "location three": 3,
            "location four":4
            }
        if rospy.get_param('~/smach/slam')==1:
            speech_text = 'Please close mapping first'
        else:
            speech_text = 'OK, just follow me, i will take you to '+navi
            ans = local.get(navi)
            rospy.set_param('~/smach/navigation',ans)
    else:
        speech_text = 'Please star navigation first'
    return question(speech_text)

@ask.intent('control',convert={'dir': str})
def control(dir):
    gogo =	{
        "forward": 1,
        "backeard": 2,
        "left": 3,
        "right":4
        }
    speech_text = ['Here you are!','Pice of cake!','Yes, my lord','command accept']
    ans = gogo.get(dir)
    rospy.set_param('~/smach/control',ans)
    return question(random.choice(speech_text))


###############################################


@ask.intent('hello',convert={'name': str})
def hello(name):
    speech_text = ['Hello ' + name,'Nice to meet you '+name,
                    'hi '+name+', how are you doing',
                    'hi '+name+', nice to meet you']
    return question(random.choice(speech_text))


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
    data = rosparam.load_file("smach.yaml",default_namespace="smach")
    #update to server
    for params, ns in data:
        rosparam.upload_params(ns,params)

def dump():
    rosparam.dump_params("smach.yaml","smach")



if __name__ == '__main__':
    init()
    app.run(debug=True)
    while True:
        if not rospy.is_shutdown():
            dump()
            reloadp()
        else:
            dump()
            print "yaml file saved"
            print "Shutting down"
            sys.exit(0)
    
