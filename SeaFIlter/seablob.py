# !usr/bin/python
# Standard imports
import cv2
import numpy as np
import math
import time

def detectBlobs(image, hsv_min, hsv_max):
     # Convertir el fotograma a formato HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Crear una máscara para detectar los píxeles azules
    mask = cv2.inRange(hsv, hsv_min, hsv_max)

    # Aplicar la máscara al fotograma original
    res = cv2.bitwise_and(image, image, mask=mask)
    kernel= cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
    np.array([[0, 0, 1, 0, 0],
       [1, 1, 1, 1, 1],
       [1, 1, 1, 1, 1],
       [1, 1, 1, 1, 1],
       [0, 0, 1, 0, 0]], dtype=np.uint8)

    blurredframe = cv2.GaussianBlur(image, (5, 5), 0)
    hsv_img = cv2.cvtColor(blurredframe, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv_img, hsv_min, hsv_max)
    mask = cv2.dilate(mask, None, iterations=1)
    mask = cv2.erode(mask, None, iterations=1)

    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
    mask = cv2.medianBlur(mask, 9) #Applying blur to minimize noise

    # Aplicar la detección de blobs
    params = cv2.SimpleBlobDetector_Params()

    params.minThreshold = 20
    params.maxThreshold = 150
    params.blobColor=255
 
    # Change distance between blobs in pixels
    params.minDistBetweenBlobs = 20
    params.minArea = 1000
    params.maxArea=300000
    params.minCircularity = 1
    params.minConvexity = 0.8
    params.minInertiaRatio = 0.001

    detector = cv2.SimpleBlobDetector_create(params)
    # Detect blobs
    reversemask = 255 - mask
    keypoints = detector.detect(mask)
    im_with_keypoints = cv2.drawKeypoints(res, keypoints, np.array([]), (0, 0, 255),
                                          cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    # Mostrar la imagen resultante
    cv2.imshow('Blue', im_with_keypoints)

    return keypoints, res

def nothing(x):
          pass
cv2.namedWindow("Trackbars")
cv2.createTrackbar("L - H", "Trackbars",90 ,100,nothing ) 
cv2.createTrackbar("L - S", "Trackbars", 50, 50,nothing)
cv2.createTrackbar("L - V", "Trackbars", 50, 50,nothing)
cv2.createTrackbar("U - H", "Trackbars", 130, 150,nothing)
cv2.createTrackbar("U - S", "Trackbars", 100, 255,nothing)
cv2.createTrackbar("U - V", "Trackbars", 100, 255, nothing)

def hsvcolors():

     l_h = cv2.getTrackbarPos("L - H", "Trackbars")
     l_s = cv2.getTrackbarPos("L - S", "Trackbars")
     l_v = cv2.getTrackbarPos("L - V", "Trackbars")
     u_h = cv2.getTrackbarPos("U - H", "Trackbars")
     u_s = cv2.getTrackbarPos("U - S", "Trackbars")
     u_v = cv2.getTrackbarPos("U - V", "Trackbars")
 
    # Set the lower and upper HSV range according to the value selected
    # by the trackbar
     hsv_min = (l_h, l_s, l_v)
     hsv_max = (u_h, u_s, u_v)
     return hsv_min, hsv_max


def getBlobRelativePosition(frame, keyPoint):
    rows = float(frame.shape[0])
    cols = float(frame.shape[1])
    center_x    = 0.5*cols
    center_y    = 0.5*rows
    # print(center_x)
    x = (keyPoint.pt[0] - center_x)/(center_x)
    y = (keyPoint.pt[1] - center_y)/(center_y)
    return(x,y)

def avoidSea(x,y,x_inflim, x_suplim):  
     x_instruction=""
     y_instruction="" 
     if x>= x_inflim and x <= x_suplim:
          if y > 0:
                    y_instruction = "Atras" 
          else:
                    y_instruction = "todo bien"  

     elif x > 0:
           x_instruction = "Izquierda, "
     elif x<0:
          x_instruction = "Derecha, "
     else:
               if y > 0:
                    y_instruction = "Atras" 
               else:
                    y_instruction = "todo bien"
           
          
     instruction = x_instruction + y_instruction
     

     return instruction

def getAngle(frame, windowSize, point):
     # WindowSize = (h,w)    point = (x,y)
     h = windowSize[0]
     w = windowSize[1]

     topPoint = (int(w/2),0)
     bottomPoint = (int(w/2), h)

     frame = cv2.line(frame, bottomPoint, topPoint, (0,0,255), 2)

     X = point[0] - int(w/2)
     Y = point[1] - 0
     angle = math.atan2(Y,X) * (180.0 / math.pi)

     return angle

def showDetectionInfo(keypoints, res, instruction, angle, line_color=(0,0,255)):
     im_with_keypoints = cv2.drawKeypoints(res
                                        , keypoints, np.array([]), line_color, cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
 
     # Show instruction to avoid
     cv2.putText(im_with_keypoints, instruction, (100, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
     cv2.imshow("DetectionInfo",im_with_keypoints)
     pass

def main():

     #Window size
     h = 480
     w = 640

     #Webcam video
     vc = cv2.VideoCapture(0)

     #Main loop
     while True:
          ret, frame = vc.read()
          if ret == True:
               hsv_min,hsv_max= hsvcolors()
               keypoints, res = detectBlobs(frame, hsv_min, hsv_max)

               for i, keyPoint in enumerate(keypoints):
                         
                         
                         #--- Here you can implement some tracking algorithm to filter multiple detections
                         #--- We are simply getting the first result
                         x = keyPoint.pt[0]
                         y = keyPoint.pt[1]
                         s = keyPoint.size
                         a = (math.pi*(s**2)) / 2

                         # Get the angle of current blob
                         angle = getAngle(frame, (h,w), (x,y))

                         #--- Find x and y position in camera adimensional frame
                         x, y = getBlobRelativePosition(frame, keyPoint)

                         # Get instruction to center the can
                         instruction = avoidSea(x, y, -0.3, 0.3)


                         # Show all the detection info in the frame
                         showDetectionInfo(keypoints, res, instruction, angle)

               if cv2.waitKey(50) == 27:
                    break

     cv2.destroyAllWindows()



if __name__ == "__main__":
     main()