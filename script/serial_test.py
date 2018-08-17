#!/usr/bin/python

import serial
import time
import sys, select, termios, tty

try:
    ser = serial.Serial('/dev/ttyUSB0' , 115200, timeout= 0.5 )
    print ("Connect success ...")
    time.sleep(1)
    try:
        print ("Flusing first 50 data readings ...")
        for x in range(0, 50):
            data = ser.read()
            time.sleep(0.01)
    except:
        print ("Flusing faile ")
        sys.exit(0)
except:
    print ("Connect faile ...")
    print (". Did you specify the correct port ?")
    sys.exit(0)

# while True:
#     try:
#         sleep(3)
#         myData = serial.readline().strip()
#         if len(myData)>0:
#             print  (myData)
#     except:
#         print ("Error in encoder value !")
#         time.sleep(1)

while True:
    try:
        myData = ser.readline(8).strip()
        if len(myData)>0:
            #print (len(myData))
            print  (myData.decode())
    except:
        print ("Error in encoder value !")
        time.sleep(1)





