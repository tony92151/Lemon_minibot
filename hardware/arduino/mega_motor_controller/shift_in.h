byte shiftIn(int myDataPin, int myClockPin);

byte switchVar1 = 0;
byte switchVar2 = 0;

uint32_t _time = 0;
static int FL = 0;
static int FR = 0;

static float WL = 0;
static float WR = 0;

int latchPin;
int dataPin;
int clockPin;
int resetPin;

int dL,dR;
int rate;

void freq_init(int LatchPin ,int DataPin, int ClockPin,int ResetPin,int DL,int DR,int Rate){
  
  latchPin = LatchPin;
  dataPin = DataPin;
  clockPin = ClockPin;
  resetPin = ResetPin;
  
  dL = DL;
  dR = DR;

  pinMode(latchPin, OUTPUT);
  pinMode(clockPin, OUTPUT);
  pinMode(dataPin, INPUT);
  pinMode(resetPin, OUTPUT);
  pinMode(dL, INPUT);
  pinMode(dR, INPUT);
  
  rate = Rate; 
}


float freq_read(int mode,float PPR){
  
  if(millis()-_time>=rate){
    _time = millis();

    //latch 
    digitalWrite(latchPin,1);
    delayMicroseconds(2);  
    digitalWrite(latchPin,0);
    //digitalWrite(resetPin,1);
    digitalWrite(resetPin,1);
    delayMicroseconds(2);
    digitalWrite(resetPin,0);

    //shift in
    switchVar1 = shiftIn(dataPin, clockPin);
    //Serial.println(switchVar1, BIN);
    switchVar2 = shiftIn(dataPin, clockPin);
    //Serial.println(switchVar2, BIN);
    
    FL = (int)switchVar1*(1000/rate);
    FR = (int)switchVar2*(1000/rate);
    WL = (float)FL/(float)PPR; //rad/s
    WR = (float)FR/(float)PPR; //rad/s
    WL = (!digitalRead(dL))?(WL):(WL*(-1.0));
    WR = (digitalRead(dR))?(WR):(WR*(-1.0));
    //return (mode)?(WL):(WR);
  }
  //digitalWrite(resetPin,0);
  //digitalWrite(latchPin,0);
  //Serial.println(digitalRead(dL));
  //Serial.print("    ");
  //Serial.println(digitalRead(dR));
  return (mode)?(WL):(WR);
}



////////////////////////////////////////////////////////////

byte shiftIn(int myDataPin, int myClockPin) { 
  int i;
  int temp = 0;
  byte myDataIn = 0;

  for (i=7; i>=0; i--){
    digitalWrite(myClockPin, 0);
    delayMicroseconds(2);
    temp = digitalRead(myDataPin);
    myDataIn = (temp)?(myDataIn | (1 << i)):(myDataIn);
    digitalWrite(myClockPin, 1);
  }
  //digitalWrite(myClockPin, 0);
  return myDataIn;
}
