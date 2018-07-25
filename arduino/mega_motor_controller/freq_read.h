

byte shiftIn(int myDataPin, int myClockPin);
 
float sum1=0, sum2=0, sum3=0;
volatile uint16_t count_L=0, count_R=0;

static int _time = 0;
static int FL = 0;
static int FR = 0;

byte switchVar1 = 0;
byte switchVar2 = 0;

static float WL = 0;
static float WR = 0;

int latchPin;
int dataPin;
int clockPin;

int dL,dR;
int rate;

void freq_init(int LatchPin ,int DataPin, int ClockPin,int DL,int DR,int Rate){
  latchPin = LatchPin;
  dataPin = DataPin;
  clockPin = ClockPin;
  
  dL = DL;
  dR = DR;

  pinMode(latchPin, OUTPUT);
  pinMode(clockPin, OUTPUT);
  pinMode(dataPin, INPUT);
  
  rate = Rate; 
}


float freq_read(int mode,int PPR){
  
  if(millis()-_time>=rate){
    _time = millis();

    //latch 
    digitalWrite(latchPin,1);  
    digitalWrite(latchPin,0);

    //shift in
    switchVar1 = shiftIn(dataPin, clockPin);
    switchVar2 = shiftIn(dataPin, clockPin);
    
    FL = (int)switchVar1*(1000/rate);
    FR = (int)switchVar2*(1000/rate);
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



////////////////////////////////////////////////////////////

byte shiftIn(int myDataPin, int myClockPin) { 
  int i;
  int temp = 0;
  int pinState;
  byte myDataIn = 0;

  for (i=11; i>=0; i--){
    digitalWrite(myClockPin, 0);
    //delayMicroseconds(2);
    temp = digitalRead(myDataPin);
    myDataIn = (temp)?(myDataIn | (1 << i)):(myDataIn);
    digitalWrite(myClockPin, 1);
  }
  return myDataIn;
}

