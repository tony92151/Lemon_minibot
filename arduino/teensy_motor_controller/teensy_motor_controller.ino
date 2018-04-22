#include "PID.h"
#include "freq_read.h"
#include "serial_print_speed.h"
#include "serial_read.h"

//left
#define motorA 5
#define motorA_ 6
#define Freq_l 6
#define DL 12

//right
#define motorB 9
#define motorB_ 10
#define Freq_r 9
#define DR 11


//motor defination
#define PPR  374.22


float motorSendL = 0;
float motorSendR = 0;
float WL_send = 0;
float WR_send = 0;

void Run(int n,int _n,int dir,int spe);

void setup() {
  freq_init(Freq_l,Freq_r,DL,DR,100);
  serialReadInit();
  PIDinit(0.1,0.5,0);//set KP,PI,KD here
  
  pinMode(DR,INPUT);
  pinMode(DL,INPUT);
  pinMode(motorA,OUTPUT);
  pinMode(motorA_,OUTPUT);
  pinMode(motorB,OUTPUT);
  pinMode(motorB_,OUTPUT);

  Serial.begin(115200);
  Serial.setTimeout(10);
  while (!Serial); 
}

void loop() {
  
  WL_send = freq_read(1,PPR);//(rad/s)
  WR_send = freq_read(0,PPR);

  printSpeed(WL_send,WR_send,100);

  motorSendL = PIDstep(1,serialRead(1),WL_send);
  motorSendR = PIDstep(0,serialRead(0),WR_send);
  Run(motorA,motorA_,(motorSendL>0)?(1):(0),abs(motorSendL));
  Run(motorB,motorB_,(motorSendR>0)?(1):(0),abs(motorSendR));
}


void Run(int n,int _n,int dir,int spe){
  (dir)?(analogWrite(n,spe),analogWrite(_n,0)):(analogWrite(_n,spe),analogWrite(n,0));
}



