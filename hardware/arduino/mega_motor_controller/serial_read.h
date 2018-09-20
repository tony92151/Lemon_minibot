static int speed_l;  
static int speed_r; 
static char buf; 
static int RW;
static char Databuf[8];     // 用來儲存收進來的 data byte  
static int addr;

void serialReadInit(){
  speed_l=0; 
  speed_r=0;
  RW=0;
  Databuf[8]={0};
  addr=0;
  Serial.begin(115200);
  Serial.setTimeout(10);
}


int serialRead(int sel){
    if (Serial.available() > 0) {
    buf = Serial.read(); 
    switch (buf){
      case '(':
        RW=1;
        break;
      case ')':
        RW=0;
        if(((int)Databuf[0]-48)!=0){
          speed_l=((int)Databuf[1]-48)*100+((int)Databuf[2]-48)*10+((int)Databuf[3]-48)*1;
        }else{
          speed_l=(((int)Databuf[1]-48)*100+((int)Databuf[2]-48)*10+((int)Databuf[3]-48)*1)*(-1);
        }
        if(((int)Databuf[4]-48)!=0){
          speed_r=((int)Databuf[5]-48)*100+((int)Databuf[6]-48)*10+((int)Databuf[7]-48)*1;
        }else{
          speed_r=(((int)Databuf[5]-48)*100+((int)Databuf[6]-48)*10+((int)Databuf[7]-48)*1)*(-1);
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
  return (!sel)?(speed_l):(speed_r);//0~100 //100 time angular speed 
}
