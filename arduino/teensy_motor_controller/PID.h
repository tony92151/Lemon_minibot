#include <FastPID.h>

float Kp=0,Ki=0,Kd=0;
int output_bits = 8;
bool output_signed = true;
bool usePID = 0; 

FastPID LPID(Kp, Ki, Kd, output_bits, output_signed);
FastPID RPID(Kp, Ki, Kd, output_bits, output_signed);

int setpoint_l;
int setpoint_r;
int feedback_l;
int feedback_r;
int output_l;
int output_r;

int time_=millis();

void PIDinit(int kp,int ki,int kd){
  usePID = 1;
  Kp = kp;
  Ki = ki;
  Kd = kd;
  LPID.setCoefficients(Kp, Ki, Kd);
  RPID.setCoefficients(Kp, Ki, Kd);
  setpoint_l = 0;
  setpoint_r = 0;
  feedback_l = 0;
  feedback_r = 0;
  output_l = 0;
  output_r = 0;
}

float PIDstep(int mode,float setpoint,float feedback){  //setpoint(rad/s) range:0~1(rad/s) ; feedback(rad/s) <all 100 time>
  if(usePID){
    (mode)?(setpoint_l = setpoint*100,feedback_l = feedback*100):(setpoint_r = setpoint*100,feedback_r = feedback*100);
    if(millis()-time_>=100){
      output_l = LPID.step(setpoint_l, feedback_l);
      output_r = RPID.step(setpoint_r, feedback_r);
      time_ = millis();
      return (mode)?(output_l):(output_r);
    }else{
      return (mode)?(output_l):(output_r);
    }
  }else{
    return (mode)?(setpoint_l*100):(setpoint_r*100);
  }
}

