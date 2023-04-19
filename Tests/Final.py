# !usr/bin/python
# Standard imports
import cv2
import numpy as np
import math
import functions as func# Our own functions file
import serial, time
def main():

     # Arduino port
     #arduino = serial.Serial("/dev/ttyACM0", 9600, timeout=1)
     # with serial.Serial("/dev/ttyACM0", 9600, timeout=1) as arduino:


     #Color range for detection!!

     #For cans
     hsv_min_black = (0, 0, 0)
     hsv_max_black = (180, 255, 30)


     #For red circle
     hsv_min_red = (136, 150, 150)
     hsv_max_red = (190, 255, 255)

     #Window size
     h = 480
     w = 640

     #Webcam video
     vc = cv2.VideoCapture(0)
  
     
     #Main loop
     while True:
          ret, frame = vc.read()

          if ret == True:
               keypoints, reversemask = func.detectBlobs(frame, hsv_min_black, hsv_max_black)
               seaCoordinate,sea = func.detectSea(frame)
               
               if seaCoordinate != (-1,-1):
                     msgAvoid = func.arduinoMessage()
               
               D = [] # list for distance of blobs
               Y=[100000]# list for ys
               instruction= "todo bien"
               visionSea= "no sea"
               #print("Buscando")
               #Sea avoid
               #instruction, visionSea = func.avoidSea(xr, y, -0.3, 0.3,h)
                    
               for keyPoint in keypoints:

                         x = keyPoint.pt[0]
                         y = keyPoint.pt[1]
                         s = keyPoint.size
                         a = (math.pi*(s**2)) / 2
                         
                         #Show blob info
                         canInfo=(int(x),int(y),int(a),int(s))
                         print(f"scan = {int(s)} x = {int(x)}  y = {int(y)}  a = {int(a)}")

           
                         # Determine minimum distance
                         dist = math.sqrt( (x - int(w/2))**2 + (y - h)**2 )
                         # Find x and y position in camera adimensional frame
                         xr, yr = func.getBlobRelativePosition(frame, keyPoint)
                         
                         D.append(dist)
                         

                         if dist <= min(D):
                              #minimal x and y
                              fX = int(x)
                              fY =int(y)

                              anglecan = func.getAngle(frame, (h,w), (fX,fY))
                              # Get instruction to center the can
                              msg = func.centerCan(anglecan)
                         

                         func.draw_target(frame,(h,w),(fX,fY))

                         # Get the angle of current blob
                         

                         # Show all the detection info in the frame
                         #func.showDetectionInfo(keypoints, frame, msg, anglecan,"Cans detected: ")

                    
          if cv2.waitKey(50) == 27:
                break

     cv2.destroyAllWindows()


if __name__ == "__main__":
     main()

