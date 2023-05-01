#!/usr/bin/env python
# -*- coding: utf-8 -*-
# lsusb to check device name
#dmesg | grep "tty" to find port name

import serial,time
import functions as func
# Serial communication
def arduinoMessage(cmd,arduino):
 
          arduino.write(cmd.encode())  
          time.sleep(0.2) #wait for arduino to answer)
          if arduino.inWaiting()>0:
               answer = str(arduino.readline())
               print(answer)
               arduino.flushInput() #remove data after reading


def main():

    #message
    msg = "led1"
    # Arduino port
    arduino = serial.Serial("/dev/ttyS0", 9600, timeout=1)
    time.sleep(0.1) #wait for serial to open
    while arduino.isOpen():
         print("Mensaje enviado 1")
         msg = "led0"
         func.arduinoMessage(msg, arduino)
         time.sleep(0.3)
         msg = "led1"
         func.arduinoMessage(msg, arduino)
         print("Mensaje enviado 2")
         time.sleep(0.3)
         
     

if __name__ == '__main__':
    main()
