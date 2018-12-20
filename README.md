# Lemon minibot

<img src="https://github.com/tony92151/Lemon_minibot/blob/master/image/IMG_3659.JPG" align="right" width="300"/>

<img src="https://github.com/tony92151/Lemon_minibot/blob/master/image/gazebo_home2.png" align="right" width="360"/>

# Hardware

Raspberry Pi3
(I use the motherboard of lenovo ideapad 100)

YDLidar X4

Arduino mega2560 & motor controller

Motor with A/B encode

14.8v li-po battery

Laser cut frame

# Software

## How to install ROS

Read my medium

https://medium.com/@tony92151/%E5%B0%88%E9%A1%8C%E7%AD%86%E8%A8%98-ros-1-c87bd92b16bc


# How to use

## Clone repositories

1.Clone this repository

> cd catkin_ws/src

> git clone https://github.com/tony92151/Lemon_minibot.git

2.Clone repository for YDLidar X4

> git clone https://github.com/EAIBOT/ydlidar

3.Clone repository for rf2o

> git clone https://github.com/MAPIRlab/rf2o_laser_odometry

4.Clone repository for smach

>git clone https://github.com/ros-visualization/executive_smach_visualization.git

5.instsll dependent

> sudo apt-get install remmina synaptic gimp git ros-kinetic-navigation ros-kinetic-amcl ros-kinetic-slam-gmapping ros-kinetic-mrpt-slam ros-kinetic-mrpt-icp-slam-2d ros-kinetic-robot-localization ros-kinetic-ar-track-alvar -y 

6.Compile all

> cd ..

> catkin_make

## Starup setting

> cd catkin_ws/src/Lemon_minibot/starup/

> sudo chmod +x initenv.sh

then enter your password

>./initenv.sh

## YDLidar X4 starup setting

> roscd ydlidar/starup/

> sudo chmod 777 ./*

> sudo sh initenv.sh

## Add ar-tag models 

> cd

> git clone https://github.com/mikaelarguedas/gazebo_models.git

> cd ar_tags/scripts/

> ./generate_markers_model.py -i ~/Documents/gazebo_models/ar_tags/images -g ~/.gazebo/models -s 80

## Simulation test

> roslaunch turtlebot3_copy turtlebot_world2.launch


If it is first time open gazebo, it will take about 10 min to download models
or you can download manual

See detial here

https://medium.com/@tony92151/%E5%AF%A6%E6%88%B0-ros-gazebo-1-bdb941f184e1

## joystick test (RONEVER SR-012)

> roslaunch joy joy2t.launch

> rostopic echo /car/cmd_vel 

<img src="https://github.com/tony92151/Lemon_minibot/blob/master/image/joy.png" width="360"/>

### Run gmapping

> roslaunch turtlebot3_copy turtlebot_world2.launch

then gazebo with minibot & home will star

> roslaunch lemon_minibot_detect ar_tag_sim.launch

to save the addres from ar-tag, run tf listener

> rosrun lemon_minibot_core ar_local.py

> roslaunch minibot_simulation simulation_gmapping.launch

to control your robot in gazebo, run keyboard_teleop.py to publish message to control node (/car/cmd_vel)

> rosrun lemon_minibot_control keyboard_teleop.py

<img src="https://github.com/tony92151/Lemon_minibot/blob/master/image/simulation_gmapping.png" width="300"/>

When mapping complete, save the map

> rosrun map_server map_saver -f ~/homemap

### run navigation

> roslaunch minibot_simulation simulation_navigation.launch map_file:=$HOME/homemap.yaml

nav goal sender

> roslaunch lemon_minibot_control movebase_seq.launch

<img src="https://github.com/tony92151/Lemon_minibot/blob/master/image/simulation_navigation.png" width="300"/>


## Smach viewer 

> rosrun smach_viewer smach_viewer.py

## set up amazom alexa skill



## Use amazon alexa

> rosrun lemon_minibot_core smach3.py

> roscd lemon_minibot_control/scripts/alexa/

> ./ngrok http 5000

and ngrok will give you the address then pastes it to "Alexa skill kit" end point

### install necessary pkg

> sudo apt-get install ngrok-client

> sudo pip install request flask flask-ask requests unidecode

### run web server to connect to amazon alexa skill

> rosrun lemon_minibot_control alexa_skill.py

> roscd lemon_minibot_control/scripts/alexa/

> ./ngrok http 5000

## Demo setup

> roscore

> roslaunch turtlebot3_copy turtlebot_world2.launch

> rosparam load ~/catkin_ws/src/Lemon_minibot/lemon_minibot_core/param/location.yaml

> rosparam load ~/catkin_ws/src/Lemon_minibot/lemon_minibot_core/param/smach.yaml

> rosrun lemon_minibot_core smach3.py

> roscd lemon_minibot_control/scripts/alexa/

> ./ngrok http 5000

> rosrun lemon_minibot_core core_controller.py

# Demo video
[![](http://img.youtube.com/vi/-EDsaaNJGFU/0.jpg)](http://www.youtube.com/watch?v=-EDsaaNJGFU "demo")

[![](http://img.youtube.com/vi/rqNOdHbekDU/0.jpg)](http://www.youtube.com/watch?v=rqNOdHbekDU "final")

# Reference

[1]turtlebot3
https://github.com/ROBOTIS-GIT/turtlebot3

[2]gazebo_models
https://github.com/mikaelarguedas/gazebo_models

[3]roslaunch API Usage
http://wiki.ros.org/roslaunch/API%20Usage

[4]Module rosparam in python
http://docs.ros.org/diamondback/api/rosparam/html/

[5]smach Tutorials
http://wiki.ros.org/smach/Tutorials/Getting%20Started


