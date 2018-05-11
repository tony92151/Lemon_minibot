#include "PID.h"
#include "freq_read.h"
#include "serial_print_speed.h"
#include "serial_read.h"

//left
#define motorA 3
#define motorA_ 4
#define Freq_l 11
#define DL 7

//right
#define motorB 5
#define motorB_ 6
#define Freq_r 12
#define DR 8


//motor defination
#define PPR  374.22
#define readRate 100 //ms  ,motor encoder read rate

//setup serial print rate
#define printRate 200 //ms


float motorSendL = 0;
float motorSendR = 0;
float WL_send = 0;
float WR_send = 0;
float serialRead_L;
float serialRead_R;

void Run(int n,int _n,int dir,int spe);

void setup() {
  freq_init(Freq_l,Freq_r,DL,DR,readRate);
  serialReadInit();
  PIDinit(5,5,3,0);//set KP,PI,KD here & pid Enable ,if disable,output will be input directly
  
  pinMode(DR,INPUT);
  pinMode(DL,INPUT);
  pinMode(motorA,OUTPUT);
  pinMode(motorA_,OUTPUT);
  pinMode(motorB,OUTPUT);
  pinMode(motorB_,OUTPUT);
  while (!Serial); 
}

void loop() {
  
  WL_send = freq_read(1,PPR);//(rad/s)
  WR_send = freq_read(0,PPR);

  printSpeed(WL_send,WR_send,printRate);

  serialRead_L = (float)serialRead(1)/100.0;
  serialRead_R = (float)serialRead(0)/100.0;

  //Serial.println(serialRead_L);
  //Serial.println(serialRead_R);

  motorSendL = (float)PIDstep(1,serialRead_L,WL_send);
  //motorSendR = (float)PIDstep(0,serialRead_R,WR_send);
  motorSendR =-100.0;

  if(motorSendR<0)Serial.println(motorSendL);
  //Serial.println(motorSendR);
  
  Run(motorA,motorA_,((int)motorSendL>0)?(1):(0),abs(motorSendL));
  //Run(motorB,motorB_,((int)motorSendR>0)?(1):(0),abs(motorSendR));

  //Serial.println(" ");
  //Serial.println(motorSendL);
  
  Run(motorA,motorA_,0,abs(motorSendR));
  //digitalWrite(motorB,HIGH);
}


void Run(int n,int _n,int dir,int spe){
  (dir)?(analogWrite(n,spe),analogWrite(_n,0)):(analogWrite(_n,spe),analogWrite(n,0));
}



