# Lemon minibot

<img src="https://github.com/tony92151/Lemon_minibot/blob/master/image/IMG_3659.JPG" align="right" width="300"/>

<img src="https://github.com/tony92151/Lemon_minibot/blob/master/image/gazebo_home.png" align="right" width="360"/>

# Hardware

lenovo ideapad 100(Raspberry Pi3)

YDLidar X4

Arduino mega2560

Motor with A/B encode

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

4.instsll dependent

> sudo apt-get install remmina synaptic gimp git ros-kinetic-navigation ros-kinetic-amcl ros-kinetic-slam-gmapping ros-kinetic-mrpt-slam ros-kinetic-mrpt-icp-slam-2d ros-kinetic-robot-localization ros-kinetic-ar-track-alvar -y 

5.Compile all

> cd ..

> catkin_make

## Starup setting

> cd catkin_ws/src/Lemon_minibot/starup/

>sudo chmod +x initenv.sh

then enter your password

>./initenv.sh

## YDLidar X4 starup setting

> roscd ydlidar/starup/

> sudo chmod 777 ./*

> sudo sh initenv.sh

## Simulation test

### run gmapping

> roslaunch turtlebot3_copy turtlebot_world2.launch

then gazebo with minibot & home will star

> roslaunch minibot_simulation simulation_gmapping.launch

to control your robot in gazebo, run keyboard_teleop.py to publish message to control node (/car/cmd_vel)

> rosrun lemon_minibot_control keyboard_teleop.py

<img src="https://github.com/tony92151/Lemon_minibot/blob/master/image/simulation_gmapping.png" width="300"/>

When mapping complete, save the map

> rosrun map_server map_saver -f ~/homemap

### run navigation

> roslaunch minibot_simulation simulation_navigation.launch map_file:=$HOME/homemap.yaml

<img src="https://github.com/tony92151/Lemon_minibot/blob/master/image/simulation_navigation.png" width="300"/>

## set up amazom alexa skill



## Use amazon alexa

### install necessary pkg

> sudo apt-get install ngrok-client

> sudo pip install request flask flask-ask requests unidecode

### run web server to connect to amazon alexa skill

> roscd lemon_minibot_control/scripts/alexa/

> ./ngrok http 5000

> rosrun lemon_minibot_control alexa_skill.py

# Demo video
[![](http://img.youtube.com/vi/WHaNt73xu4k/0.jpg)](http://www.youtube.com/watch?v=WHaNt73xu4k "demo video")

[![](http://img.youtube.com/vi/vS1muTZ_ens/0.jpg)](http://www.youtube.com/watch?v=vS1muTZ_ens "short cut")
