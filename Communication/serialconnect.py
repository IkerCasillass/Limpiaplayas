#!/usr/bin/env python
# -*- coding: utf-8 -*-
# lsusb to check device name
#dmesg | grep "tty" to find port name

import serial,time

# Serial communication
def arduinoMessage(cmd):
     
    with serial.Serial("/dev/ttyAMA0", 9600, timeout=1) as arduino:
        time.sleep(0.1) #wait for serial to open
        if arduino.isOpen():
            print("{} connected!".format(arduino.port))
            try:
                while True:
                    arduino.write(cmd.encode())
                    #time.sleep(0.1) #wait for arduino to answer
                    while arduino.inWaiting()==0: pass
                    if  arduino.inWaiting()>0: 
                        answer=arduino.readline()
                        print(answer)
                        arduino.flushInput() #remove data after reading
            except KeyboardInterrupt:
                print("KeyboardInterrupt has been caught.")


def main():

    #message
    msg = "led0"
    # Arduino port
    # with serial.Serial("/dev/ttyACM0", 9600, timeout=1) as arduino:
    time.sleep(0.1) #wait for serial to open

    #Main loop
    while True:
        if msg == "led0":
            msg = "led1"
            arduinoMessage(msg)
            time.sleep(2.0)
        else:
            msg == "led0"
            arduinoMessage(msg)
            time.sleep(1.0)

if __name__ == '__main__':
    main()
