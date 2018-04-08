#!/usr/bin/python
import serial
arduinoData = serial.Serial('/dev/ttyUSB0' , 115200, timeout= 0.5)
while (1):
        myData = (arduinoData.readline().strip()) 
        if len(myData)>0:
            XL  = int(myData[1])*100+int(myData[2])*10+int(myData[3])
            XR = int(myData[5])*100+int(myData[6])*10+int(myData[7])
            XL = float(XL)/100.0
            XR = float(XR)/100.0
            if int(myData[0])<1:
                XL = XL*(-1)
            if int(myData[4])<1:
                XR = XR*(-1)
            print XL
            print XR
