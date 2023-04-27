# !usr/bin/python
# Standard imports
import cv2 
from math import pi, sqrt
import functions as func# Our own functions file
import serial 
import time


def main(): 

     # Arduino port
     # with serial.Serial("/dev/ttyACM0", 9600, timeout=1) as arduino:
     arduino = serial.Serial("/dev/ttyACM0", 9600, timeout=1)
     time.sleep(0.1) #wait for serial to open
     msg = 'B' #empty message

     #Window size
     #h = 480
     #w = 640
     winSize = (640,480) #width,height (x,y)

     #Webcam video
     vc = cv2.VideoCapture(0)

     #check for conection
     if arduino.isOpen():
          print("{} connected!".format(arduino.port))
          func.arduinoMessage(msg, arduino)

     #Main loop
     while arduino.isOpen():

          ret, frame = vc.read()
          cv2.imshow("image",frame)
          vc.set(cv2.CAP_PROP_FPS, 30)
          if ret:
               #IDLE STATE
               #Sea detection
               seaCoordinate, sea = func.detectSea(frame)
               cv2.imshow("sea", sea)
               # If sea is close enough
               if seaCoordinate[1] > winSize[1]/3:
                    # Get angle and send message to avoid sea
                    seaAngle = func.getAngle(winSize, seaCoordinate)
                    msg = func.avoidSea(seaAngle)
                    print("sea " + msg)
                    func.arduinoMessage(msg, arduino)
               #Can detection
               canP, canFlag = func.get_Cans(frame, winSize)
               #can detected
               if canFlag:
                    canAngle = func.getAngle(winSize, canP)
                    msg = func.centerBlob(canAngle)
                    print("can " + msg)
                    func.arduinoMessage(msg, arduino)
               if seaCoordinate == (-1,-1) and canFlag == False:
                    func.arduinoMessage('L', arduino)
                    print("looking")
               #time.sleep(0.2)

          if cv2.waitKey(50) == 27:
               break

     cv2.destroyAllWindows()


if __name__ == "__main__":
     main()

