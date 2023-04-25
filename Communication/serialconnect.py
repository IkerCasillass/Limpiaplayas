#!/usr/bin/env python
# -*- coding: utf-8 -*-
# lsusb to check device name
#dmesg | grep "tty" to find port name

import serial,time

# Serial communication
def arduinoMessage(cmd,arduino):
     #with serial.Serial("/dev/ttyACM0", 9600, timeout=1) as arduino:
         # print("{} connected!".format(arduino.port))
          '''if arduino.isOpen():
               print("recheck connection")'''
          arduino.write(cmd.encode())

	#arduino.write(cmd.encode())
               #print("msg received")  
          time.sleep(0.2) #wait for arduino to answer
          #else: print("msg not send")
         
              # print(arduino.inWaiting())
         # while arduino.inWaiting() == 0:pass
                   # print("waiting")
              # arduino.write(cmd.encode())
              # print("Mensaje guardado")
               #time.sleep(2.0)
               #if  arduino.inWaiting()>0:
          answer=str(arduino.readline())
          #print("respuesta guardada")
          #print("Mensaje: "+answer)
          #print(len(answer))
          print(answer)
          arduino.flushInput() #remove data after reading


def main():

    #message
    msg = "led1"
    # Arduino port
    # with serial.Serial("/dev/ttyACM0", 9600, timeout=1) as arduino:
    time.sleep(0.1) #wait for serial to open

    #check for conection
    #if arduino.isOpen():
       # print("{} connected!".format(arduino.port))

    #Main loop
    #while arduino.isOpen():
    #while True:
    '''if msg == "led0":
         arduinoMessage(msg,arduino)
         msg = "led1"
       else:
         arduinoMessage(msg,arduino)
         msg = "led0"'''
    
    arduinoMessage(msg,arduino)
    print("dummy")
    time.sleep(1.0)
    arduinoMessage(msg,arduino)

     

if __name__ == '__main__':
    main()
