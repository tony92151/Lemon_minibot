#include <FreqMeasureMulti.h>
//#include <Adafruit_NeoPixel.h>

FreqMeasureMulti freq_l;
FreqMeasureMulti freq_r;

 
float sum1=0, sum2=0, sum3=0;
int count1=0, count2=0, count3=0;

static int _time=millis();
static int FL = 0;
static int FR = 0;
static float WL = 0;
static float WR = 0;
int dL,dR;
int rate;

void freq_init(int left ,int right,int DL,int DR,int Rate){
  freq_l.begin(left);
  freq_r.begin(right);
  dL = DL;
  dR = DR;
  rate = Rate;
  //freq_l.begin(6);
  //freq_r.begin(9);
}

float freq_read(int mode,int PPR){
  if (freq_l.available()) {
    sum1 = sum1 + freq_l.read();
    count1 = count1 + 1;
  }
  if (freq_r.available()) {
    sum2 = sum2 + freq_r.read();
    count2 = count2 + 1;
  }
  if(millis()-_time>=rate){
    _time = millis();
    FL = (int)freq_l.countToFrequency(sum1 / count1);
    FR = (int)freq_r.countToFrequency(sum2 / count2);
    WL = (float)FL/(float)PPR; //rad/s
    WR = (float)FR/(float)PPR; //rad/s
    (digitalRead(dL))?(WL = WL):(WL = WL*(-1));
    (digitalRead(dR))?(WR = WR):(WR = WR*(-1));
    sum1 = 0;
    sum2 = 0;
    count1 = 0;
    count2 = 0; 
    return (mode)?(WL):(WR);
  }
  return (mode)?(WL):(WR);
}


