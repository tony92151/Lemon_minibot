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

> sudo apt-get install remmina synaptic gimp git ros-kinetic-navigation ros-kinetic-amcl ros-kinetic-slam-gmapping ros-kinetic-mrpt-slam ros-kinetic-mrpt-icp-slam-2d ros-kinetic-robot-localization -y

5.Compile all

> cd ..

> catlin_make

## Startup setting

> cd catkin_ws/src/Lemon_minibot/startup

>sudo chmod +x initenv.sh

then enter your password

>./initenv.sh

## YDLidar X4 startup setting

> roscd ydlidar/startup

> sudo chmod 777 ./*

> sudo sh initenv.sh


[![](http://img.youtube.com/vi/WHaNt73xu4k/0.jpg)](http://www.youtube.com/watch?v=WHaNt73xu4k "demo video")
