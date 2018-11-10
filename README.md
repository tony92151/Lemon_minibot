# Lemon minibot

<img src="https://github.com/tony92151/Lemon_minibot/blob/master/image/IMG_3659.JPG" align="right" width="300"/>

<img src="https://github.com/tony92151/Lemon_minibot/blob/master/image/gazebo_home.png" align="right" width="300"/>

# Hardware

Raspberry Pi3

YDLidar X4

Arduino mega2560

Motor with A/B encode

# Software

For raspberry pi 2/3

https://medium.com/@tony92151/%E5%B0%88%E9%A1%8C%E7%AD%86%E8%A8%98-ros-1-c87bd92b16bc

$sudo apt-get install remmina synaptic gimp git ros-kinetic-navigation ros-kinetic-amcl ros-kinetic-slam-gmapping ros-kinetic-mrpt-slam ros-kinetic-mrpt-icp-slam-2d ros-kinetic-robot-localization -y

# How to use
1.Clone this repository

> cd catkin_ws/sec

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

[![](http://img.youtube.com/vi/WHaNt73xu4k/0.jpg)](http://www.youtube.com/watch?v=WHaNt73xu4k "demo video")
