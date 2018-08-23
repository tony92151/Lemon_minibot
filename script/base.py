#!/usr/bin/python

import serial
import time
import sys, select, termios, tty
import rospy
import tf
import math
import string
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry


class BaseControl:
    def __init__(self):        
        self.odom_freq = float( rospy.get_param('~odom_freq', '50') ) # hz of odom pub
        self.odom_topic = rospy.get_param('~odom_topic', '/odom') # topic name
        self.baseId = rospy.get_param('~base_id', 'base_footprint') # base link
        self.odomId = rospy.get_param('~odom_id', 'odom') # odom link
        self.VxCov = float( rospy.get_param('~vx_cov', '1.0') ) # covariance for Vx measurement
        self.VyawCov = float( rospy.get_param('~vyaw_cov', '1.0') ) # covariance for Vyaw measurement
        self.pub_tf = bool(rospy.get_param('~pub_tf', True)) # whether publishes TF or not
        self.wheelRad = float(0.068/2.0) #m
        self.wheelSep = float(0.17) #m

        try:
            self.serial = serial.Serial('/dev/mega_controller' , 115200, timeout= 0.5 )
            rospy.loginfo("Connect success ...")

            try:
                print ("Flusing first 50 data readings ...")
                for x in range(0, 50):
                    data = self.serial.read()
                    time.sleep(0.01)
            except:
                print ("Flusing faile ")
                sys.exit(0)

        except serial.serialutil.SerialException:
            rospy.logerr("Can not receive data from the port: "#+ self.device_port + 
            ". Did you specify the correct port ?")
            self.serial.close
            sys.exit(0) 
        rospy.loginfo("Communication success !")

        # rospy.loginfo("Flusing first 50 data readings ...")
        #     for x in range(0, 50):
        #         self.serial.readline().strip()
        #         time.sleep(0.01)

        # ROS handler        
        self.sub = rospy.Subscriber('/car/cmd_vel', Twist, self.cmdCB, queue_size=10)
        self.pub = rospy.Publisher(self.odom_topic, Odometry, queue_size=10)


        self.timer_odom = rospy.Timer(rospy.Duration(1.0/10), self.timerOdomCB)
        self.timer_cmd = rospy.Timer(rospy.Duration(0.1), self.timerCmdCB) # 10Hz
        self.tf_broadcaster = tf.TransformBroadcaster()


        # variable        
        self.trans_x = 0.0 # cmd
        self.rotat_z = 0.0
        self.WL_send = 0.0
        self.WR_send = 0.0
        self.current_time = rospy.Time.now()
        self.previous_time = rospy.Time.now()
        self.pose_x = 0.0 # SI
        self.pose_y = 0.0
        self.pose_yaw = 0.0
        # self.WL = 0
        # self.WR = 0
     
    def cmdCB(self, data):
        self.trans_x = data.linear.x
        self.rotat_z = data.angular.z

    #################################################################################################

    def timerOdomCB(self, event):
        # Serial read & publish 
        try:
            myData = self.serial.readline(8).strip()
            if len(myData)>0:
            	WL = int(myData[1])*100+int(myData[2])*10+int(myData[3])
            	WR = int(myData[5])*100+int(myData[6])*10+int(myData[7])
            	WL = float(WL)/100.0
            	WR = float(WR)/100.0
            	if int(myData[0])<1:
	                WL = WL*(-1)
                if int(myData[4])<1:
	                WR = WR*(-1)
                rospy.loginfo(myData)
            #print "serialRead success~"
            # Twist
            VL = WL * self.wheelRad*6 # V = omega * radius, unit: m/s
            VR = WR * self.wheelRad*6
            Vyaw = (VR-VL)/self.wheelSep
            Vx = (VR+VL)/2.0
            #print "Twist success~"

            # Pose
            self.current_time = rospy.Time.now()
            dt = (self.current_time - self.previous_time).to_sec()
            self.previous_time = self.current_time
            self.pose_x   = self.pose_x   + Vx * math.cos(self.pose_yaw) * dt
            self.pose_y   = self.pose_y   + Vx * math.sin(self.pose_yaw) * dt
            self.pose_yaw = self.pose_yaw + Vyaw * dt
            pose_quat = tf.transformations.quaternion_from_euler(0,0,self.pose_yaw)

            #print "Pose success~"
            
            # Publish Odometry
            msg = Odometry()
            msg.header.stamp = self.current_time
            msg.header.frame_id = self.odomId
            msg.child_frame_id  = self.baseId
            msg.pose.pose.position.x = self.pose_x
            msg.pose.pose.position.y = self.pose_y
            msg.pose.pose.position.z = 0.0
            msg.pose.pose.orientation.x =  pose_quat[0]
            msg.pose.pose.orientation.y =  pose_quat[1]
            msg.pose.pose.orientation.z =  pose_quat[2]
            msg.pose.pose.orientation.w =  pose_quat[3]
            msg.twist.twist.linear.x = Vx
            msg.twist.twist.angular.z = Vyaw

            #print "Odometry pub success~"

            for i in range(36):
                msg.twist.covariance[i] = 0
            msg.twist.covariance[0] = self.VxCov
            msg.twist.covariance[35] = self.VyawCov
            msg.pose.covariance = msg.twist.covariance
            self.pub.publish(msg)

            #print "pub success~"

            # TF Broadcaster
            if self.pub_tf:
                self.tf_broadcaster.sendTransform( (self.pose_x, self.pose_y, 0.0), pose_quat, self.current_time, self.baseId, self.odomId)          

            
        except: 
            rospy.loginfo("Error in encoder value !") 
            pass


    #################################################################################################

    def timerCmdCB(self, event):

        self.WR_send = int(self.trans_x - self.wheelSep*self.rotat_z*2)
        self.WL_send = int(self.trans_x + self.wheelSep*self.rotat_z*2)
        # rospy.logerr("WR_send: "+ chr(self.WR_send))
        # rospy.logerr("WL_send: "+ chr(self.WL_send))       
        if self.WR_send < 0:
            R_forward = 0
        else:
        	R_forward = 1
        if self.WL_send < 0:
            L_forward = 0
        else:
        	L_forward = 1
    	self.WR_send = abs(self.WR_send)
    	self.WL_send = abs(self.WL_send)
        if self.WR_send > 255:
            self.WR_send = 255
        if self.WL_send > 255:
            self.WL_send = 255
        self.WL_send = str(self.WL_send)
        self.WR_send = str(self.WR_send)
        while len(self.WL_send)<3:
        	self.WL_send = "0"+self.WL_send
    	while len(self.WR_send)<3:
        	self.WR_send = "0"+self.WR_send
        #output = chr(255) + chr(254) + chr(self.WL_send) + chr(L_forward) + chr(self.WR_send) + chr(R_forward)   
        output = "(" + str(L_forward) + str(self.WL_send) + str(R_forward) + str(self.WR_send)+")"     
        #print output     
        #rospy.loginfo(output.encode())
        self.serial.write(output)

        
if __name__ == "__main__":
    try:    
        # ROS Init    
        rospy.init_node('base_control', anonymous=True)

        # Constract BaseControl Obj
        rospy.loginfo("Bot Base Control ...")
        bc = BaseControl()
        rospy.spin()
    except KeyboardInterrupt:    
        bc.serial.close        
        print("Shutting down")
