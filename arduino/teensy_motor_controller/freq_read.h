//#include <FreqMeasureMulti.h>
//#include <Adafruit_NeoPixel.h>

//FreqMeasureMulti freq_l;
//FreqMeasureMulti freq_r;

 
float sum1=0, sum2=0, sum3=0;
volatile uint16_t count_L=0, count_R=0;

static int _time = 0;
static int FL = 0;
static int FR = 0;
static float WL = 0;
static float WR = 0;
int dL,dR;
int rate;

void interrupt_L(){count_L++;}
void interrupt_R(){count_R++;}

void freq_init(int left ,int right,int DL,int DR,int Rate){
  //freq_l.begin(left);
  //freq_r.begin(right);
  dL = DL;
  dR = DR;
  rate = Rate;
  //freq_l.begin(6);
  //freq_r.begin(9);
  attachInterrupt(digitalPinToInterrupt(left), interrupt_L, FALLING);
  attachInterrupt(digitalPinToInterrupt(right), interrupt_R, FALLING);
  
}


float freq_read(int mode,int PPR){
  
  if(millis()-_time>=rate){
    _time = millis();
    FL = count_L*(1000/rate);
    FR = count_R*(1000/rate);
    WL = (float)FL/(float)PPR; //rad/s
    WR = (float)FR/(float)PPR; //rad/s
    WL = (digitalRead(dL))?(WL):(WL*(-1));
    WR = (digitalRead(dR))?(WR):(WR*(-1));
    count_L = 0;
    count_R = 0; 
    //return (mode)?(WL):(WR);
  }
  return (mode)?(WL):(WR);
}


