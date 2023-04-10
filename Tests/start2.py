# !usr/bin/python
# Standard imports
import cv2
import numpy as np
import math
import functions2 as func# Our own functions file

def main():
     #Color range for detection!!

     #For cans
     hsv_min_black = (0, 0, 0)
     hsv_max_black = (180, 255, 30)

     #For sea
     hsv_min_blue = (99, 132, 90)
     hsv_max_blue = (136, 255, 255)

     #For red circle
     hsv_min_red = (136, 150, 150)
     hsv_max_red = (190, 255, 255)

     #Window size
     h = 480
     w = 640

     #Webcam video
     #vc = cv2.VideoCapture(0)
     ret=True
     src = "PLAA4.jpg"
     
     #Main loop
     while True:
          frame = cv2.imread(src,1)

          #ret, frame = vc.read()
          if ret == True:
               keypoints, reversemask = func.detectBlobs(frame, hsv_min_black, hsv_max_black)
               keypointsb, res = func.detectSea(frame, hsv_min_blue, hsv_max_blue)
               keypointsc, mask= func.detectBlobs(frame, hsv_min_red, hsv_max_red)
               D = [] # list for distance of blobs
               Y=[]# list for ys
               instruction= "todo bien"
               visionSea= "no sea"

               for keyPoint in keypointsb:
                         
                         x = keyPoint.pt[0]
                         y = keyPoint.pt[1]
                         s = keyPoint.size
                         a = (math.pi*(s**2)) / 2
                         y= y

                         seainfo=(int(x),int(y),int(a),int(s))
                         print(f"ssea = {int(s)} x = {int(x)}  y = {int(y)}  a = {int(a)}")
                         x , y = func.getBlobRelativePosition(frame, keyPoint)

                         Y.append(y)
                         if y <= min(Y):
                              #minimal x and y
                              SX = int(x)
                              SY = int(y)
                              # Get instruction to center the can
                              instruction, visionSea = func.avoidSea(x, y, -0.3, 0.3)
                    

                         print(visionSea)

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
                              # Get instruction to center the can
                              instructionCan,visionCan = func.centerCan(xr, yr, -0.3, 0.3)
                         
                         if instruction== "todo bien":
                            print(instructionCan)
                         else:
                            print(instruction)  

                         func.draw_target(frame,(h,w),(fX,fY))

                         # Get the angle of current blob
                         angle = func.getAngle(frame, (h,w), (fX,fY))

                         # Show all the detection info in the frame
                         func.showDetectionInfo(keypoints, frame, instructionCan, angle)

                         cv2.imshow("redmask", mask)
                         print(visionCan)
                    
               
               for keyPoint in keypointsc:

                         x = keyPoint.pt[0]
                         y = keyPoint.pt[1]
                         s = keyPoint.size
                         a = (math.pi*(s**2)) / 2
                         
                         #Show blob info
                         redInfo=(int(x),int(y),int(a),int(s))
                         print(f"s = {int(x)} x = {int(y)}  y = {int(a)}  a = {int(s)}")

                         xr, yr = func.getBlobRelativePosition(frame, keyPoint)

                         # Get instruction to center the can
                         instructionhoop,visionhoop = func.centerHoop(fX, fY, -0.3, 0.3)
                         print("Vision:" + visionCan+","+visionSea+","+visionhoop)
                         

                         if instruction== "todo bien" and instructionCan== "Centered,Avanza 1":
                            print(instructionhoop)

                         func.draw_target(frame,(h,w),(fX,fY))

                         # Get the angle of current blob
                         angle = func.getAngle(frame, (h,w), (fX,fY))

                         # Show all the detection info in the frame
                         func.showDetectionInfo(keypoints, frame, instructionCan, angle)


               
               if cv2.waitKey(50) == 27:
                    break

     cv2.destroyAllWindows()


if __name__ == "__main__":
     main()