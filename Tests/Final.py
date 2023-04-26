# !usr/bin/python
# Standard imports
import cv2 
from math import pi, sqrt
import functions as func# Our own functions file
import serial, time


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

     #Main loop
     while arduino.isOpen():

          ret, frame = vc.read()
          cv2.imshow("image",frame)
          vc.set(cv2.CAP_PROP_FPS, 30)
          if ret:
               keypoints, reversemask = func.detectCans(frame)
               cv2.imshow("cans", reversemask)
               seaCoordinate, sea = func.detectSea(frame)
               
               #if seaCoordinate != (-1,-1):
                    #msg = func.arduinoMessage()
               
               D = [] # list for distance of blobs

               #print("Buscando")
               #Sea avoid
               #instruction, visionSea = func.avoidSea(xr, y, -0.3, 0.3,h)
               if keypoints != []: 
                   for keyPoint in keypoints:

                       x = keyPoint.pt[0]
                       y = keyPoint.pt[1]
                       s = keyPoint.size
                       a = (pi*(s**2)) / 2
                    
                    #Show blob info
                    #print(f"scan = {int(s)} x = {int(x)}  y = {int(y)}  a = {int(a)}")
          
                       # Determine minimum distance
                       dist = sqrt( (x - int(winSize[0]/2))**2 + (y - winSize[1])**2 )
                    
                       D.append(dist)
                    

                       if dist <= max(D):
                         #minimal x and y
                         fX = int(x)
                         fY = int(y)

                         anglecan = func.getAngle(frame, winSize, (fX,fY))
                         func.draw_target(frame,winSize,(fX,fY))
                         # Get instruction to center the can
                         msg = func.centerBlob(anglecan)
                         #print(msg)
                         if msg != 'C':
                              func.arduinoMessage(msg,arduino)
                         elif msg == 'C':
                              func.arduinoMessage(msg,arduino)
               else: 
                    func.arduinoMessage('B',arduino)
               #func.arduinoMessage('B',arduino)    
                    #
                    #func.draw_target(frame,(h,w),(fX,fY))

                    # Get the angle of current blob
                    

                    # Show all the detection info in the frame
                    #func.showDetectionInfo(keypoints, frame, msg, anglecan,"Cans detected: ")
                    #     
          if cv2.waitKey(50) == 27:
                break

     cv2.destroyAllWindows()


if __name__ == "__main__":
     main()

