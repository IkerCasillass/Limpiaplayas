# !usr/bin/python
# Standard imports
import cv2
import numpy as np
import math
import serial, time 

# mathematical funtions
def getAngle(windowSize, point):
     # WindowSize = (h,w)    point = (x,y)
     h = windowSize[1]
     w = windowSize[0]

     topPoint = (int(w/2),0)
     bottomPoint = (int(w/2), h)

     X = point[0] - int(w/2)
     Y = point[1] - 0
     angle = math.atan2(Y,X) * (180.0 / math.pi)

     return angle

def getBlobRelativePosition(frame, keyPoint):

    rows = float(frame.shape[0])
    cols = float(frame.shape[1])
    center_x    = 0.5*cols
    center_y    = 0.5*rows

    x = (keyPoint.pt[0] - center_x)/(center_x)
    y = (keyPoint.pt[1] - center_y)/(center_y)
    return(x,y)

#Functions for blob detection
def detectCans(image):
    
    # masks For cans
     hsv_min_black = (0, 0, 0)
     hsv_max_black = (180, 255, 30)

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

     blurredframe = cv2.GaussianBlur(image, (5,5), 0)
     hsv_img = cv2.cvtColor(blurredframe, cv2.COLOR_BGR2HSV)

     mask = cv2.inRange(hsv_img, hsv_min_black, hsv_max_black)
     mask = cv2.dilate(mask, None, iterations=1)
     mask = cv2.erode(mask, None, iterations=1)

     mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
     mask = cv2.medianBlur(mask, 9) #Applying blur to minimize noise

     # Detect blobs.
     reversemask = 255 - mask

     keypoints = detector.detect(reversemask)
     
     return keypoints, reversemask

def get_Cans(img, shape):
     h = shape[1]
     w = shape[0]

     # convert the image to grayscale
     gray_image = img.copy()
     gray_image = cv2.cvtColor(gray_image, cv2.COLOR_BGR2GRAY)
     blur = cv2.GaussianBlur(gray_image,(11,11),cv2.BORDER_DEFAULT)

     # convert the grayscale image to binary image
     thresh = cv2.threshold(blur,60,250,cv2.THRESH_BINARY_INV)[1]
     
     # find contours in the binary image
     contours = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[0]
     
     D = []
     if contours != []:
          for c in contours:
               # calculate moments for each contour
               M = cv2.moments(c)
               if M["m00"]!=0:
                    # calculate x,y coordinate of center
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
               else:
                    cX = 0
                    cY = 0
               #cv2.circle(img, (cX, cY), 5, (255, 255, 255), -1)
               #cv.putText(img, "centroid", (cX - 25, cY - 25),cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
               dist = math.sqrt( (cX - int(w/2))**2 + (cY - h)**2 )
               D.append(dist)
               if dist <= min(D):
                    #minimal x and y
                    fX = cX
                    fY = cY
                    #draw all targets
                    #draw_target(img,(h,w),(fX,fY))
          return (fX,fY), True
     else:
          return (-1,-1), False
          

def centerBlob(angle, type):
     rango = 20

     if type == "can": 
          # Checar si esta centrada
          if angle < 90 + rango and angle > 90 - rango:
               #print("centered")
               # can centered -> Collect  
               return 'CC'
          
          if angle < 90 - rango: #can right
               #print("derecha")
               return 'CR'
          
          elif angle > 90 + rango: #can left
               #print("izquierda")
               return 'CL'
     elif type == "hoop":
          # Checar si esta centrado
          if angle < 90 + rango and angle > 90 - rango: #hoop centered
               #print("centered")
               return 'HC'
          
          if angle < 90 - rango: #hoop right
               #print("derecha")
               return 'HR'
          
          elif angle > 90 + rango: #hoop left
               #print("izquierda")
               return 'HL'

     
def collectCan(y, h, collectedCans):
     message = ""

     if y < 2/3*h: #can detected
          message = "CD"

     # Si se encuentra suficinetemente cerca
     elif y > 2/3*h: #can hard forward
          message = "CF"
          collectedCans += 1

     return message, collectedCans

# Debbug functions
def draw_target(frame, windowSize, point):

     if point[0] == 0 or point[1] == 0:
          return
     # Start coordinate at the bottom of the image (w/2, 0)
     h = windowSize[1]
     w = windowSize[0]
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

     cv2.imshow("target",image)

def showDetectionInfo(keypoints, frame, instruction, angle, variable, line_color=(0,0,255)):
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
     

     cv2.imshow(variable, im_with_keypoints)
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

    
    #For storing y coordinates of sea
    maxY = 0
    X = 0
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

               # Obtener coordenada mas cercana al robot
               if y > maxY:
                    maxY = y
                    X = x

          i += 1

    coordinates = (X, maxY)

    if coordinates != (0,0):
         return coordinates, sea
    else:
         return (-1, -1), sea
    
def avoidSea(angle):
     # Checar si esta centrada
     
     if angle <= 90: #sea right
          #print(" mar derecha")
          return "SR"
     
     elif angle > 90: #sea left
          #print("mar izquierda")
          return "SL"
     
# Hoop    
def detectHoop(img):
     imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
     hsv_min_red = (169, 140, 0) #lower red mask
     hsv_max_red = (179, 255, 255) #upper red mask

     kernel = np.ones((11, 11), np.uint8)
     redMask = cv2.inRange(imgHSV,hsv_min_red,hsv_max_red)
     opening = cv2.morphologyEx(redMask, cv2.MORPH_OPEN, kernel, iterations=3)
     closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)

     hoop =  cv2.bitwise_and(img, img, mask=closing)

     grayimg = cv2.cvtColor(hoop, cv2.COLOR_BGR2GRAY)

          # Detecting contours in image. 
     contours, _= cv2.findContours(grayimg, cv2.RETR_TREE, 
                                   cv2.CHAIN_APPROX_SIMPLE)
     
     #For storing y coordinates of the hoop
     maxY = 0
     promX = 0
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
                    promX += n[i] 
                    y = n[i + 1]

                    # Obtener coordenada mas cercana al robot
                    if y > maxY:
                         maxY = y
               i = i + 1

          promX /= len(n)

     coordinates = (promX, maxY)

     if coordinates != (0,0):
          return coordinates, hoop
     else:
          return (-1, -1), hoop
     
def depositHoop(y, h, collectedCans):
     message = ""
     
     #si se encuentra lejos que avance
     if y <= 2/3*h: #hoop detected
          message = "HD"

     # Si se encuentra suficientemente cerca deposite en el hoop
     elif y > 2/3*h: #hoop throw (deposit)
          message = "HT"
          collectedCans = 0

     return message, collectedCans

# Serial communication
def arduinoMessage(cmd,arduino):

     arduino.write(cmd.encode())
     time.sleep(0.2) #wait for arduino to answer
     #answer=str(arduino.readline())
     #print(answer)
     arduino.flushInput() #remove data after reading 
