#include <ros/ros.h>
#include <geometry_msgs/Twist.h>
#include <sensor_msgs/Joy.h>

# include <iostream>
using namespace std ;

class TeleopTurtle
{
public:
  TeleopTurtle();

private:
  void joyCallback(const sensor_msgs::Joy::ConstPtr& joy);

  ros::NodeHandle nh_;

  int linearX_,linearY_, angular_;
  double l_scale_, a_scale_;
  ros::Publisher vel_pub_;
  ros::Subscriber joy_sub_;

};


TeleopTurtle::TeleopTurtle():
  linearX_(1),
  linearY_(0),
  angular_(3)
{

  nh_.param("axisX_linear", linearX_, linearX_);
  nh_.param("axisY_linear", linearY_, linearY_);
  nh_.param("axis_angular", angular_, angular_);
  nh_.param("scale_angular", a_scale_, a_scale_);
  nh_.param("scale_linear", l_scale_, l_scale_);


  vel_pub_ = nh_.advertise<geometry_msgs::Twist>("car/cmd_vel", 1);


  joy_sub_ = nh_.subscribe<sensor_msgs::Joy>("joy", 10, &TeleopTurtle::joyCallback, this);

}

void TeleopTurtle::joyCallback(const sensor_msgs::Joy::ConstPtr& joy)
{
  geometry_msgs::Twist twist;
  twist.angular.z = (a_scale_*joy->buttons[angular_]>a_scale_*joy->buttons[angular_-2])?(a_scale_*joy->buttons[angular_]*(-1)):(a_scale_*joy->buttons[angular_-2]);
  //twist.angular.z = (a_scale_*joy->buttons[angular_])*(a_scale_*joy->buttons[angular_-2]);
  twist.linear.x = l_scale_*joy->axes[linearX_];
  twist.linear.y = l_scale_*joy->axes[linearY_];
  vel_pub_.publish(twist);
  //cout << joy<< endl ;
}


int main(int argc, char** argv)
{
  ros::init(argc, argv, "teleop_turtle");
  TeleopTurtle teleop_turtle;

  ros::spin();
}
