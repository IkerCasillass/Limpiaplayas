# !usr/bin/python
# Standard imports
import cv2
import numpy as np
import math
import functions as func# Our own functions file

def main():
     #Color range for detection!!!!!

     #For cans
     hsv_min_black = (0, 0, 0)
     hsv_max_black = (180, 255, 30)

     #For sea
     hsv_min_blue = (99, 132, 90)
     hsv_max_blue = (136, 255, 255)

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
               D = [] # list for distance of blobs

               for keyPoint in keypoints:

                         x = keyPoint.pt[0]
                         y = keyPoint.pt[1]
                         s = keyPoint.size
                         a = (math.pi*(s**2)) / 2
                         
                         #Show blob info
                         print(f"s = {int(s)} x = {int(x)}  y = {int(y)}  a = {int(a)}")

                         #--- Find x and y position in camera adimensional frame
                         xr, yr = func.getBlobRelativePosition(frame, keyPoint)
          
                         # Get instruction to center the can
                         instruction = func.centerCan(xr, yr, -0.3, 0.3)
                         #instructionSea = avoidSea(xr, yr, -0.3, 0.3)

                         # Determine minimum distance
                         dist = math.sqrt( (x - int(w/2))**2 + (y - h)**2 )
                         D.append(dist)
                         if dist <= min(D):
                              #minimal x and y
                              fX = int(x)
                              fY = int(y)
                         func.draw_target(frame,(h,w),(fX,fY))

                         # Get the angle of current blob
                         angle = func.getAngle(frame, (h,w), (fX,fY))

                         # Show all the detection info in the frame
                         func.showDetectionInfo(keypoints, frame, instruction, angle)

                         cv2.imshow("mask", reversemask)
               if cv2.waitKey(50) == 27:
                    break

     cv2.destroyAllWindows()


if __name__ == "__main__":
     main()