/**
 *  Name : mega_motor_controller
 *
 *  Author : Tony Guo
 *  
 *  Country : Taiwan
 *
 *  Date : 15 Aug, 2018 
 */



#include "PID.h"
#include "shift_in.h"
#include "serial_print_speed.h"
#include "serial_read.h"


//left
#define motorA 2
#define motorA_ 3
//#define Freq_l 11
#define DL 6
#define pwmA 12

//right
#define motorB 4
#define motorB_ 5
//#define Freq_r 12
#define DR 7
#define pwmB 11


//motor defination
#define PPR  374.22
#define readRate 100 //ms  ,motor encoder read rate

//setup serial print rate
#define printRate 100 //ms


float motorSendL = 0;
float motorSendR = 0;
float WL_send = 0;
float WR_send = 0;
float serialRead_L;
float serialRead_R;

int LatchPin = 8;
int DataPin = 10;
int ClockPin = 9;
int ResetPin = 13;

void Run(int n,int _n,int moto,int dir,int spe);

void setup() {
  //freq_init(latchPin,dataPin,clockPin,DL,DR,readRate);
  serialReadInit();
  PIDinit(5,5,3,0);//set KP,PI,KD here & pid Enable ,if disable,output will be input directly
  freq_init(LatchPin,DataPin,ClockPin,ResetPin,DR,DL,100);//LatchPin,DataPin,ClockPin,ResetPin,DL,DR,Rate

  pinMode(DR,INPUT);
  pinMode(DL,INPUT);
  pinMode(motorA,OUTPUT);
  pinMode(motorA_,OUTPUT);
  pinMode(motorB,OUTPUT);
  pinMode(motorB_,OUTPUT);
  while (!Serial); 
}

void loop() {
  
  WL_send = freq_read(0,PPR);//(rad/s)  //0:left
  WR_send = freq_read(1,PPR);           //1:right

  //Serial.print(WL_send);
  //Serial.print("   ");
  //Serial.println(WR_send);

  printSpeed(WL_send,WR_send,printRate);

  serialRead_L = (float)serialRead(0)/100.0; //0:left
  serialRead_R = (float)serialRead(1)/100.0; //1:right

  //Serial.println(serialRead_L);
  //Serial.println(serialRead_R);

  motorSendL = (float)PIDstep(1,serialRead_L,WL_send);
  motorSendR = (float)PIDstep(0,serialRead_R,WR_send);
  //motorSendR =-100.0;

  //Serial.println(motorSendL);
  //Serial.println(motorSendR);

  //if(motorSendR<0)Serial.println(motorSendL);
  //Serial.println(motorSendR);
  
  Run(motorA,motorA_,pwmA,((int)motorSendL>0)?(0):(1),abs(motorSendL));
  Run(motorB,motorB_,pwmB,((int)motorSendR>0)?(1):(0),abs(motorSendR));

  //Serial.println(" ");
  //Serial.println(motorSendL);
  
  //Run(motorA,motorA_,pwmA,0,100); //(pin)pwmA control left motor
  //Run(motorB,motorB_,pwmB,1,100); //(pin)pwmB control right motor
  //digitalWrite(motorB,HIGH);
  
}


void Run(int n,int _n,int moto,int dir,int spe){
  if(dir){
    digitalWrite(n,HIGH);
    digitalWrite(_n,LOW);
    analogWrite(moto,spe);
  }else{
    digitalWrite(n,LOW);
    digitalWrite(_n,HIGH);
    analogWrite(moto,spe); 
  }
  //(dir)?(analogWrite(n,spe),analogWrite(_n,0)):(analogWrite(_n,spe),analogWrite(n,0));
}


