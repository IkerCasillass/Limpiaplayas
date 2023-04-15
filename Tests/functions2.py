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
     x_instruction=""
     if x >= x_inflim and x <= x_suplim:
          instruction = "Centered"
          visionCan= ("centered can in vision")
     else:
          if x > 0:
               x_instruction = "Derecha, "
               visionCan= ("Can in the right")
     
          else:
               x_instruction = "Izquierda, "
               visionCan= ("Can in the left")
     
          instruction = x_instruction 
     
     return instruction,visionCan

def collectCan(y,collectedCans):
     y_instruction=""
     if y < 0:
          y_instruction = ",Avanza"
          visionCan= ("Can at the top")
     else:
          y_instruction = ",Avanza +1"
          visionCan= ("Can at the bottom")
          collectedCans =collectedCans+1
     return y_instruction,visionCan,collectedCans


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

def showDetectionInfo(keypoints, frame, instruction, angle,variable, line_color=(0,0,255)):
     im_with_keypoints = cv2.drawKeypoints(frame
                                        , keypoints, np.array([]), line_color, cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
     # Show keypoints
     text = variable + str(len(keypoints))
     cv2.putText(im_with_keypoints, text, (20, 350),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
     
     # Show angle
     text = "angle: " + str(round(angle, 2)) # Angle with 2 decimals
     cv2.putText(im_with_keypoints, text, (200, 240),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (170, 255, 0), 2)
     
     # Show instruction to center
     cv2.putText(im_with_keypoints, instruction, (100, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
     

     cv2.imshow(variable,im_with_keypoints)
     pass

# Functions for sea
def detectSea(img): #Returns lowest point of sea and sea mask
    blueHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lowerBlue = np.array([90, 153, 0], np.uint8) #lower blue mask
    upperBlue = np.array([120, 255, 255], np.uint8) #upper blue mask

    kernel = np.ones((11, 11), np.uint8)
    blueMask = cv2.inRange(blueHSV,lowerBlue,upperBlue)
    opening = cv2.morphologyEx(blueMask, cv2.MORPH_OPEN, kernel, iterations=3)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)

    sea =  cv2.bitwise_and(img, img, mask=closing)

    grayimg = cv2.cvtColor(sea, cv2.COLOR_BGR2GRAY)
        # Detecting contours in image. 
    contours, _= cv2.findContours(grayimg, cv2.RETR_TREE, 
                                cv2.CHAIN_APPROX_SIMPLE) 
    

    font = cv2.FONT_HERSHEY_COMPLEX
    
    #For storing y coordinates of sea
    xcoordinates=[]
    ycoordinates = []
    # Going through every contours found in the image. 
    for cnt in contours : 

        approx = cv2.approxPolyDP(cnt, 0.009 * cv2.arcLength(cnt, True), True) 

        # draws boundary of contours. 
        cv2.drawContours(img, [approx], 0, (0, 0, 255), 5) 

        # Used to flatted the array containing 
        # the co-ordinates of the vertices. 
        n = approx.ravel() 
        i = 0


        for j in n : 
            
            if(i % 2 == 0): 
                x = n[i] 
                y = n[i + 1]
                xcoordinates.append(x) 
                ycoordinates.append(y)    
                columns = float(img.shape[1])
                center_x    = 0.5*columns
                xr = (x - center_x)/(center_x)
                
                # String containing the co-ordinates. 
                string = str(x) + " " + str(y) 

            i = i + 1

    if len(ycoordinates) != 0:
          return max(ycoordinates),min(xcoordinates), sea
    else:
          return -1,-1, sea

def avoidSea(x,y,x_inflim,x_suplim,h):
          x_instruction=""
          y_instruction=""
          if y> h/2: 
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
          visionHoop= ("Centered hoop in vision")
     else:
          if x > 0:
               instruction = "Derecha, "
               visionHoop= ("Hoop in the right")
          else:
               instruction = "Izquierda, "
               visionHoop= ("Hoop in the left")
     
     return instruction, visionHoop
     
def depositHoop(x,y,x_inflim, x_suplim):
     if y < 0:
               y_instruction = "Avanza 1"
               visionCan= ("Hoop far")
     else:
               y_instruction = "Retrocede 1"
               instruction = y_instruction
               
     return instruction,visionCan
