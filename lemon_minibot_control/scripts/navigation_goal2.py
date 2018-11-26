#!/usr/bin/env python
# license removed for brevity
__author__ = 'fiorellasibona'

# reference http://www.hotblackrobotics.com/en/blog/2018/01/29/seq-goals-py/

import rospy
import math

import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from actionlib_msgs.msg import GoalStatus
from geometry_msgs.msg import Pose, Point, Quaternion
from tf.transformations import quaternion_from_euler
import sys


class MoveBaseSeq():

    def __init__(self):

        
        #points_seq = rospy.get_param('move_base_seq/p_seq')

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

        self.navigation = int(rospy.get_param('~/smach/navigation'))
        #0:none, 1:location1, 2:location2 ,etc

        # Only yaw angle required (no ratotions around x and y axes) in deg:
        yaweulerangles_seq = rospy.get_param('move_base_seq/yea_seq')
        #List of goal quaternions:
        quat_seq = list()
        #List of goal poses:
        self.pose_seq = list()
        self.goal_cnt = 0
        for yawangle in yaweulerangles_seq:
            #Unpacking the quaternion tuple and passing it as arguments to Quaternion message constructor
            quat_seq.append(Quaternion(*(quaternion_from_euler(0, 0, yawangle*math.pi/180, axes='sxyz'))))
        n = 3
        # Returns a list of lists [[point1], [point2],...[pointn]]
        #points = [points_seq[i:i+n] for i in range(0, len(points_seq), n)]
        points=[[self.local1_x,self.local1_y,0],
                [self.local2_x,self.local2_y,0],
                [self.local3_x,self.local3_y,0],
                ]
        rospy.loginfo(str(points))
        for point in points:
            #Exploit n variable to cycle in quat_seq
            self.pose_seq.append(Pose(Point(*point),quat_seq[n-3]))
            n += 1
        rospy.loginfo(str(self.pose_seq))
        #Create action client
        self.client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
        rospy.loginfo("Waiting for move_base action server...")
        wait = self.client.wait_for_server(rospy.Duration(5.0))
        if not wait:
            rospy.logerr("Action server not available!")
            rospy.signal_shutdown("Action server not available!")
            return
        rospy.loginfo("Connected to move base server")
        rospy.loginfo("Starting goals achievements ...")
        

    def active_cb(self):
        rospy.loginfo("Goal pose "+str(self.goal_cnt+1)+" is now being processed by the Action Server...")

    def feedback_cb(self, feedback):
        #rospy.loginfo("Feedback for goal "+str(self.goal_cnt)+": "+str(feedback))
        rospy.loginfo("Feedback for goal pose "+str(self.goal_cnt+1)+" received")
        self.navigation = -1

    def done_cb(self, status, result):
        #self.goal_cnt += 1
    # Reference for terminal status values: http://docs.ros.org/diamondback/api/actionlib_msgs/html/msg/GoalStatus.html
        if status == 2:
            rospy.loginfo("Goal pose "+str(self.goal_cnt)+" received a cancel request after it started executing, completed execution!")

        if status == 3:
            rospy.loginfo("Waiting for goal!!")
            self.navigation = 0
            rospy.set_param('/smach/navigation',self.navigation)
            # rospy.loginfo("Goal pose "+str(self.goal_cnt)+" reached") 
            # if self.goal_cnt< len(self.pose_seq):
            #     next_goal = MoveBaseGoal()
            #     next_goal.target_pose.header.frame_id = "map"
            #     next_goal.target_pose.header.stamp = rospy.Time.now()
            #     next_goal.target_pose.pose = self.pose_seq[self.goal_cnt]
            #     print(self.goal_cnt)
            #     rospy.loginfo("Sending goal pose "+str(self.goal_cnt+1)+" to Action Server!!")
            #     rospy.loginfo(str(self.pose_seq[self.goal_cnt]))
            #     self.client.send_goal(next_goal, self.done_cb, self.active_cb, self.feedback_cb) 
            # else:
            #     rospy.loginfo("Final goal pose reached!")
            #     rospy.signal_shutdown("Final goal pose reached!")
            #     return

        if status == 4:
            rospy.loginfo("Goal pose "+str(self.goal_cnt)+" was aborted by the Action Server")
            rospy.signal_shutdown("Goal pose "+str(self.goal_cnt)+" aborted, shutting down!")
            return

        if status == 5:
            rospy.loginfo("Goal pose "+str(self.goal_cnt)+" has been rejected by the Action Server")
            rospy.signal_shutdown("Goal pose "+str(self.goal_cnt)+" rejected, shutting down!")
            return

        if status == 8:
            rospy.loginfo("Goal pose "+str(self.goal_cnt)+" received a cancel request before it started executing, successfully cancelled!")
            print "Shutting down"
            sys.exit(0)

    def update(self):
        self.navigation = int(rospy.get_param('~/smach/navigation'))
    
    def movebase_client(self):
    #for pose in pose_seq:   
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = "map"
        goal.target_pose.header.stamp = rospy.Time.now() 
        print "**********************************************"
        print "value:"
        print ("navigation {  %d  }" % (self.navigation))  #0:none, 1:location1, 2:location2 ,etc
        print "**********************************************"
        
        
        if self.navigation==0:
            rospy.loginfo("Waiting for goal!")
            rospy.sleep(0.5)
        else:
            goal.target_pose.pose = self.pose_seq[self.navigation]
            rospy.loginfo("Sending goal pose "+str(self.navigation)+" to Action Server")
            rospy.loginfo(str(self.pose_seq[self.navigation]))
            self.client.send_goal(goal, self.done_cb, self.active_cb, self.feedback_cb)
            while self.navigation!=0:
                rospy.sleep(0.1)
        

if __name__ == '__main__':
    rospy.init_node('move_base_sequence')
    mb=MoveBaseSeq()
    while True:
        if not rospy.is_shutdown():
            mb.movebase_client() 
            mb.update()
        else:
            rospy.loginfo("Navigation finished.")
            print "Shutting down"
            sys.exit(0)

        
