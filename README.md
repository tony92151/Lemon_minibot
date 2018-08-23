# Lemon minibot


Hardware

Raspberry Pi3

YDLidar X4

Arduino mega2560

Motor with A/B encode

Software

For raspberry pi 2/3

https://medium.com/@tony92151/%E5%B0%88%E9%A1%8C%E7%AD%86%E8%A8%98-ros-1-c87bd92b16bc

$sudo apt-get install remmina synaptic gimp git ros-kinetic-navigation ros-kinetic-amcl ros-kinetic-slam-gmapping ros-kinetic-mrpt-slam ros-kinetic-mrpt-icp-slam-2d ros-kinetic-robot-localization -y

For YDLidar X4

$ cd catkin_ws/src

$ git clone https://github.com/EAIBOT/ydlidar


For joystick

$ git clone https://github.com/tony92151/joystick_drivers.git

For rf2o

$ git clone https://github.com/MAPIRlab/rf2o_laser_odometry

For lemon minibot

$ git clone https://github.com/tony92151/Lemon_minibot.git

Compile All

$ cd ..

$ catlin_make
