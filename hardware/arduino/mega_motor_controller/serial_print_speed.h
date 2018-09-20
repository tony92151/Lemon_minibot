uint32_t Time = millis();

void printSpeed(float WL,float WR,int rate){
  if(millis()-Time>=rate){
    Time = millis();
    int IWR = abs(WR)*100; //turn 100 time float type to int type 
    int IWL = abs(WL)*100;
    String SWR = (String)IWR;
    String SWL = (String)IWL;
    while(SWR.length()<3){SWR = '0'+SWR;}
    while(SWL.length()<3){SWL = '0'+SWL;}

    SWL = (WL>0)?('1'+SWL):('0'+SWL);
    SWR = (WR>0)?('1'+SWR):('0'+SWR);
    
    //(WR>0)?(SWR ='0'+SWR):(SWR ='1'+SWR);
    //(!WL>0)?(SWL ='0'+SWL):(SWL ='1'+SWL);
  
    //(!WR>0)?(SWR ='0'+SWR):(SWR ='1'+SWR); //if need to invert
    //(!WL>0)?(SWL ='0'+SWL):(SWL ='1'+SWL); //if need to invert
  
    Serial.println(SWL+SWR);
    Serial.flush();
    if(0){ //debug option
      Serial.print(" WL= ");
      Serial.print(SWL);
      Serial.print(" WR= ");
      Serial.print(SWR);
      Serial.println(" (rad/s) ");
    }
  }
}
