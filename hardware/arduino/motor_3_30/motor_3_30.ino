#define motorB 5
#define motorB_ 6 //left
#define motorA 9
#define motorA_ 10 //right

#define FL 2 //left
#define FR 3 //right
#define DL 12 //left
#define DR 11 //right

volatile uint8_t STEP_R = 0; 
volatile uint8_t STEP_L = 0;
volatile float  WR = 0;
volatile float  WL = 0;  
volatile uint16_t Time = 0; 
String DDR,DDL; 

///////////////////////////////////////////////////////////////////////////////
// Interrupt func
void Freq_int_L(){STEP_L++;}
void Freq_int_R(){STEP_R++;}


void Run(int n,int _n,int dir,int spe);
int Read(int sel);//sel=1 >>left  sel=0 >>right



void setup() {
  pinMode(FR,INPUT_PULLUP);
  pinMode(FL,INPUT_PULLUP);
  pinMode(DR,INPUT);
  pinMode(DL,INPUT);
  attachInterrupt(digitalPinToInterrupt(FL),Freq_int_L,RISING);
  attachInterrupt(digitalPinToInterrupt(FR),Freq_int_R,RISING);
  pinMode(motorA,OUTPUT);
  pinMode(motorA_,OUTPUT);
  pinMode(motorB,OUTPUT);
  pinMode(motorB_,OUTPUT);
  Serial.begin(115200);
  Serial.setTimeout(20);
}

void loop() {
  
  Run(motorA,motorA_,(Read(1)>0)?(1):(0),abs(Read(1)));
  Run(motorB,motorB_,(Read(0)>0)?(1):(0),abs(Read(0)));

  if(millis()-Time>=100){
    WR = ((float)STEP_R/374.22)*10.0; //rad/s
    WL = ((float)STEP_L/374.22)*10.0; //rad/s
    STEP_R = 0;
    STEP_L = 0;
    int IWR = WR*100;
    int IWL = WL*100;
    String SWR = (String)IWR;
    String SWL = (String)IWL;
    while(SWR.length()<3){SWR = '0'+SWR;}
    while(SWL.length()<3){SWL = '0'+SWL;}
    (!digitalRead(DR))?(SWR ='0'+SWR):(SWR ='1'+SWR);
    (digitalRead(DL))?(SWL ='0'+SWL):(SWL ='1'+SWL);

    Serial.println(SWR+SWL);
//    Serial.print("VL=");
//    Serial.print(VL);
//    Serial.print("  VR=");
//    Serial.println(VR);
    Time = millis();
  }
}

int Read(int sel){
    static int speed_l=0;  
    static int speed_r=0; 
    static char buf; 
    static int RW=0;
    static char Databuf[8]={0};     // 用來儲存收進來的 data byte  
    static int addr=0;
    if (Serial.available() > 0) {
    buf = Serial.read(); 
    switch (buf){
      case '(':
        RW=1;
        break;
      case ')':
        RW=0;
        if(((int)Databuf[0]-48)==0){
          speed_r=((int)Databuf[1]-48)*100+((int)Databuf[2]-48)*10+((int)Databuf[3]-48)*1;
        }else{
          speed_r=(((int)Databuf[1]-48)*100+((int)Databuf[2]-48)*10+((int)Databuf[3]-48)*1)*(-1);
        }
        if(((int)Databuf[4]-48)==0){
          speed_l=((int)Databuf[5]-48)*100+((int)Databuf[6]-48)*10+((int)Databuf[7]-48)*1;
        }else{
          speed_l=(((int)Databuf[5]-48)*100+((int)Databuf[6]-48)*10+((int)Databuf[7]-48)*1)*(-1);
        }
        addr=0;
        break;
      case '!':
          for(int i=0;i<=7;i++){
            Serial.print("Databuf ") ;
            Serial.print(i) ;
            Serial.print("= ") ;
            Serial.println(Databuf[i]); 
          }

          Serial.println(speed_l);
          Serial.println(speed_r);
          addr=0;
        break;
      default:  
        if(RW==1){
          Databuf[addr]=buf;
          addr++;  
        }
        break;
    }
  }
  if(sel){
    return speed_l;
  }else{
    return speed_r;
  }
}

void Run(int n,int _n,int dir,int spe){
  (dir)?(analogWrite(n,spe),analogWrite(_n,0)):(analogWrite(_n,spe),analogWrite(n,0));
}








