#include <PID_v1.h>

//#include <FastPID.h>

double Kp=2, Ki=5, Kd=1;
uint16_t deadband = 0;
int output_bits = 8;
bool output_signed = true;
int usePID ; 

double setpoint_l;
double setpoint_r;
double feedback_l;
double feedback_r;
double output_l;
double output_r;

PID LPID(&feedback_l, &output_l, &feedback_l, Kp, Ki, Kd, DIRECT);
PID RPID(&feedback_r, &output_r, &setpoint_r, Kp, Ki, Kd, DIRECT);

int time_=millis();

void PIDinit(double kp,double ki,double kd,int usepid){
  usePID = 1;
  Kp = kp;
  Ki = ki;
  Kd = kd;
  LPID.SetTunings(Kp, Ki, Kd);
  RPID.SetTunings(Kp, Ki, Kd);
  LPID.SetMode(AUTOMATIC);
  RPID.SetMode(AUTOMATIC);
  setpoint_l = 0;
  setpoint_r = 0;
  feedback_l = 0;
  feedback_r = 0;
  output_l = 0;
  output_r = 0;
  usePID = usepid;
}

float PIDstep(int mode,float setpoint,float feedback){  //setpoint(rad/s) range:0~1(rad/s) ; feedback(rad/s) <all 100 time>
  if(usePID){
    (mode)?(setpoint_l = setpoint*100.0,feedback_l = feedback*100.0):(setpoint_r = setpoint*100.0,feedback_r = feedback*100.0);
    if(millis()-time_>=100){
      LPID.Compute();
      RPID.Compute();
      time_ = millis();
      if(0){ //debug option
        Serial.println(setpoint_l);
        Serial.println(output_l);
        Serial.println(setpoint_r);
        Serial.println(output_r);
      }
      //return (mode)?(output_l):(output_r);
    }
    return (mode)?(output_l):(output_r);
  }else{
    return setpoint*100;
  }
}

