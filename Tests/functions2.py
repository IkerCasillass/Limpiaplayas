# !usr/bin/python
# Standard imports
import cv2
import numpy as np
import math

#Functions for blob detection

def detectBlobs(image, hsv_min, hsv_max):

    # Setup SimpleBlobDetector parameters.
    params = cv2.SimpleBlobDetector_Params()

    # Change thresholds for binarizing image
    params.minThreshold = 0
    params.maxThreshold = 150

    # Change distance between blobs in pixels
    params.minDistBetweenBlobs = 20

    # Filter by Color. (0-255 in binary scale)
    params.filterByColor = True
    params.blobColor = 0

    # Filter by Area. (meassured in density pixels)
    params.filterByArea = True
    params.minArea = 1000
    params.maxArea = 40000

    # Filter by Circularity (values between 0 - 1)
    params.filterByCircularity = False
    #params.minCircularity = 0
    #params.maxCircularity = 1

    # Filter by Convexity (values from 0 to 1)
    params.filterByConvexity = False
    params.minConvexity = 0.87
    params.maxConvexity = 1
    
    # Filter by Inertia (values from 0 to 1 -> circle)
    params.filterByInertia = False
    params.minInertiaRatio = 0.1
    params.maxInertiaRatio = 0.5

    # Create a detector with the parameters
    detector = cv2.SimpleBlobDetector_create(params)

    #Definir Kernel para operaciones morfologicas (open - close)
    kernel = np.ones((5, 5), np.uint8)

    blurredframe = cv2.GaussianBlur(image, (5, 5), 0)
    hsv_img = cv2.cvtColor(blurredframe, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv_img, hsv_min, hsv_max)
    mask = cv2.dilate(mask, None, iterations=1)
    mask = cv2.erode(mask, None, iterations=1)

    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
    mask = cv2.medianBlur(mask, 9) #Applying blur to minimize noise

    # Detect blobs.
    reversemask = 255 - mask

    keypoints = detector.detect(reversemask)
    
    return keypoints, reversemask

def getBlobRelativePosition(frame, keyPoint):
    rows = float(frame.shape[0])
    cols = float(frame.shape[1])
    center_x    = 0.5*cols
    center_y    = 0.5*rows

    x = (keyPoint.pt[0] - center_x)/(center_x)
    y = (keyPoint.pt[1] - center_y)/(center_y)
    return(x,y)
     
def centerCan(x,y,x_inflim, x_suplim):
     y_instruction=""
     x_instruction=""
     if x >= x_inflim and x <= x_suplim:
          instruction = "Centered"
          visionCan= ("centered can in vision")

          if y < 0:
               y_instruction = ",Avanza 3"
               visionCan= ("Can at the top")
          else:
               y_instruction = ",Avanza 1"
               visionCan= ("Can at the bottom")

     else:
          if x > 0:
               x_instruction = "Izquierda, "
               visionCan= ("Can in the right")
     
          else:
               x_instruction = "Derecha, "
               visionCan= ("Can in the left")
     
          instruction = x_instruction + y_instruction
     
     return instruction,visionCan

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

def draw_target(frame, windowSize, point):

    if point[0] == 0 or point[1] == 0:
        return
    # Start coordinate at the bottom of the image (w/2, 0)
    h = windowSize[0]
    w = windowSize[1]
    start_point = (int(w/2), h)
    
    # End coordinate, blob
    end_point = (point[0], point[1])
    
    # Green color in BGR
    color = (255, 0, 0)
    
    # Line thickness of 9 px
    thickness = 3
    
    # Using cv2.line() method
    # Draw a diagonal green line with thickness of 9 px
    image = cv2.line(frame, start_point, end_point, color, thickness)

    pass

def showDetectionInfo(keypoints, frame, instruction, angle, line_color=(0,0,255)):
     im_with_keypoints = cv2.drawKeypoints(frame
                                        , keypoints, np.array([]), line_color, cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
     # Show keypoints
     text = "Cans detected: " + str(len(keypoints))
     cv2.putText(im_with_keypoints, text, (20, 350),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
     
     # Show angle
     text = "angle: " + str(round(angle, 2)) # Angle with 2 decimals
     cv2.putText(im_with_keypoints, text, (200, 240),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (170, 255, 0), 2)
     
     # Show instruction to center
     cv2.putText(im_with_keypoints, instruction, (100, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

     cv2.imshow("DetectionInfo",im_with_keypoints)
     pass

# Functions for sea
def detectSea(image, hsv_min, hsv_max):
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
 
    params.minDistBetweenBlobs = 20
    params.minArea = 1000
    params.maxArea=300000
    params.minCircularity = 1
    params.minConvexity = 0.8
    params.minInertiaRatio = 0.001

    detector = cv2.SimpleBlobDetector_create(params)

    keypoints = detector.detect(mask)
    im_with_keypoints = cv2.drawKeypoints(res, keypoints, np.array([]), (0, 0, 255),
                                          cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    # Mostrar la imagen resultante
    cv2.imshow("blue",im_with_keypoints)
    return keypoints, res

def avoidSea(x,y,x_inflim,x_suplim):
          x_instruction=""
          y_instruction=""
          if y> 0: 
               if x>= x_inflim and x <= x_suplim:
                    y_instruction = "Atras" 
                    vision= ("El mar está cerca y centrado")
               elif x > 0:
                    x_instruction = "Izquierda, "
                    vision= ("El mar está a la derecha y cerca")  
               elif x <0:
                    x_instruction = "Derecha, "
                    vision= ("El mar está a la izquierda y cerca")  
          else:
               y_instruction = "todo bien"
               vision=("El mar está relativamente lejos")  
     
          instruction = x_instruction + y_instruction
     
          return instruction, vision
    

def centerHoop(x,y,x_inflim, x_suplim):
     if x >= x_inflim and x <= x_suplim:
          instruction = "Centered, drop can"
          visionCan= ("Centered hoop in vision")
     else:
          if x > 0:
               x_instruction = "Izquierda, "
               visionCan= ("Hoop in the left")
          else:
               x_instruction = "Derecha, "
               visionCan= ("Hoop in the right")
     
          if y < 0:
               y_instruction = " Hoop Arriba, avanza 1"
               visionCan= ("Hoop far")
          else:
               y_instruction = "Hoop Abajo, retrocede 1"
          instruction = x_instruction + y_instruction

     return instruction,visionCan